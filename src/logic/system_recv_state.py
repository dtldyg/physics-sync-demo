# coding=utf-8

import base.math as math
import base.ecs as ecs


class SystemRecvState(ecs.System):
	def __init__(self):
		super(SystemRecvState, self).__init__((ecs.LABEL_PACKAGE, ecs.LABEL_TRANSFORM))

	def update(self, dt, component_tuples):
		for eid, comp_tuple in component_tuples:
			comp_package, comp_transform = comp_tuple
			for pkg in comp_package.packages:
				comp_transform.server_position = math.Vector(**pkg['p'])
				comp_transform.server_velocity = math.Vector(**pkg['v'])
				comp_transform.server_modified = True
