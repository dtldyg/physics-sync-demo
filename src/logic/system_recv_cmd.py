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
			opt = -1
			if comp_package.buffer_state == 0:
				if buffer_size <= const.NETWORK_SERVER_BUFFER_MIN:
					opt = 1
				elif buffer_size >= const.NETWORK_SERVER_BUFFER * 2 - const.NETWORK_SERVER_BUFFER_MIN:
					opt = 2
			else:
				if (comp_package.buffer_state == 1 and buffer_size >= const.NETWORK_SERVER_BUFFER) or \
						(comp_package.buffer_state == 2 and buffer_size <= const.NETWORK_SERVER_BUFFER):
					opt = 0
			if opt >= 0:
				comp_package.buffer_state = opt
				comp_connection.send_q.put({'pid': net.PID_BUFFER, 'opt': opt})
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
