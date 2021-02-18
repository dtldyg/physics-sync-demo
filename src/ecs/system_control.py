# coding=utf-8

import common.base.math as math
import ecs.system as system
import ecs.component as component


class SystemControl(system.System):
	def __init__(self):
		super(SystemControl, self).__init__((component.LABEL_PACKAGE, component.LABEL_CONTROL))

	def update(self, dt, component_tuples):
		for eid, component_tuple in component_tuples:
			component_package, component_control = component_tuple
			for pkg in component_package.packages:
				component_control.frame = pkg['fr']
				if pkg['f']['x'] == 0 and pkg['f']['y'] == 0:
					component_control.force_normal = math.vector_zero
				else:
					component_control.force_normal = math.Vector(**pkg['f']).normal()
