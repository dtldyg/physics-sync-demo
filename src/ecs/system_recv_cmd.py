# coding=utf-8

import common.base.math as math
import ecs.system as system
import ecs.component as component


class SystemRecvCmd(system.System):
	def __init__(self):
		super(SystemRecvCmd, self).__init__((component.LABEL_PACKAGE, component.LABEL_PHYSICS, component.LABEL_FRAME))

	def update(self, dt, component_tuples):
		for eid, component_tuple in component_tuples:
			component_package, component_physics, component_frame = component_tuple
			for pkg in component_package.packages:
				component_frame.frame = pkg['fr']
				if pkg['f']['x'] == 0 and pkg['f']['y'] == 0:
					component_physics.force_normal = math.vector_zero
				else:
					component_physics.force_normal = math.Vector(**pkg['f']).normal()
