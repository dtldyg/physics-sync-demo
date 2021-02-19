# coding=utf-8

import time
import common.base.math as math
import ecs.system as system
import ecs.component as component


class SystemRecvState(system.System):
	def __init__(self):
		super(SystemRecvState, self).__init__((component.LABEL_PACKAGE, component.LABEL_TRANSFORM, component.LABEL_RENDER))

	def update(self, dt, component_tuples):
		for eid, component_tuple in component_tuples:
			component_package, component_transform, component_render = component_tuple
			for pkg in component_package.packages:
				component_transform.server_position = math.Vector(**pkg['p'])
				component_transform.server_velocity = math.Vector(**pkg['v'])
				server_interpolation = component_render.server_interpolation
				server_interpolation[0], server_interpolation[1] = server_interpolation[2], server_interpolation[3]
				server_interpolation[2], server_interpolation[3] = component_transform.server_position, time.time()
