# coding=utf-8

import base.net as net
import base.math as math
import base.ecs as ecs
import base.const as const


class SystemRecvCmd(ecs.System):
	def __init__(self):
		super(SystemRecvCmd, self).__init__((ecs.LABEL_PACKAGE, ecs.LABEL_PHYSICS, ecs.LABEL_FRAME, ecs.LABEL_CONNECTION))

	def update(self, dt, component_tuples):
		for eid, comp_tuple in component_tuples:
			comp_package, comp_physics, comp_frame, comp_connection = comp_tuple
			for pkg in comp_package.packages:
				comp_package.buffer.put(pkg)
			buffer_size = comp_package.buffer.qsize()
			# buffer adjust
			if comp_package.buffer_state == 0:
				if buffer_size <= const.NETWORK_SERVER_BUFFER_MIN:
					comp_package.buffer_state = 1
					comp_connection.send_q.put({'pid': net.PID_BUFFER, 'opt': 1})
				elif buffer_size >= const.NETWORK_SERVER_BUFFER * 2 - const.NETWORK_SERVER_BUFFER_MIN:
					comp_package.buffer_state = 2
					comp_connection.send_q.put({'pid': net.PID_BUFFER, 'opt': 2})
			elif comp_package.buffer_state == 1:
				if buffer_size >= const.NETWORK_SERVER_BUFFER:
					comp_package.buffer_state = 0
					comp_connection.send_q.put({'pid': net.PID_BUFFER, 'opt': 0})
			elif comp_package.buffer_state == 2:
				if buffer_size <= const.NETWORK_SERVER_BUFFER:
					comp_package.buffer_state = 0
					comp_connection.send_q.put({'pid': net.PID_BUFFER, 'opt': 0})
			# pop one pkg
			pkg = None
			if comp_package.buffer.qsize() > 0:
				pkg = comp_package.buffer.get()
			if pkg is not None:
				comp_frame.frame = pkg['fr']
				if pkg['f']['x'] == 0 and pkg['f']['y'] == 0:
					comp_physics.force_normal = math.vector_zero
				else:
					comp_physics.force_normal = math.Vector(**pkg['f']).normal()
