# coding=utf-8

import queue
import base.math as math
import base.ecs as ecs
import base.const as const


class SystemRecvCmd(ecs.System):
	def __init__(self):
		super(SystemRecvCmd, self).__init__((ecs.LABEL_PACKAGE, ecs.LABEL_PHYSICS, ecs.LABEL_FRAME))

	def update(self, dt, component_tuples):
		for eid, comp_tuple in component_tuples:
			comp_package, comp_physics, comp_frame = comp_tuple
			if not comp_package.buffer_init:
				comp_package.buffer_init = True
				for _ in range(const.NETWORK_SERVER_BUFFER):
					comp_package.buffer.put(None)
			for pkg in comp_package.packages:
				comp_package.buffer.put(pkg)
			# TODO remove
			if comp_package.buffer.qsize() == 0:
				print(0)
			if comp_package.buffer.qsize() > 0:
				pkg = comp_package.buffer.get()
			else:
				pkg = None
			if pkg is not None:
				comp_frame.frame = pkg['fr']
				if pkg['f']['x'] == 0 and pkg['f']['y'] == 0:
					comp_physics.force_normal = math.vector_zero
				else:
					comp_physics.force_normal = math.Vector(**pkg['f']).normal()
