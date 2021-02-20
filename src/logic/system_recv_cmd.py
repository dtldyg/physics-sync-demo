# coding=utf-8

import base.math as math
import base.ecs as ecs


class SystemRecvCmd(ecs.System):
	def __init__(self):
		super(SystemRecvCmd, self).__init__((ecs.LABEL_PACKAGE, ecs.LABEL_PHYSICS, ecs.LABEL_FRAME))

	def update(self, dt, component_tuples):
		for eid, comp_tuple in component_tuples:
			comp_package, comp_physics, comp_frame = comp_tuple
			for pkg in comp_package.packages:
				comp_frame.frame = pkg['fr']
				if pkg['f']['x'] == 0 and pkg['f']['y'] == 0:
					comp_physics.force_normal = math.vector_zero
				else:
					comp_physics.force_normal = math.Vector(**pkg['f']).normal()
