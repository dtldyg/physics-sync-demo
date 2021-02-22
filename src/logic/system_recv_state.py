# coding=utf-8

import time
import base.math as math
import base.ecs as ecs


class SystemRecvState(ecs.System):
	def __init__(self):
		super(SystemRecvState, self).__init__((ecs.LABEL_PACKAGE, ecs.LABEL_TRANSFORM, ecs.LABEL_RENDER))

	def update(self, dt, component_tuples):
		for eid, comp_tuple in component_tuples:
			comp_package, comp_transform, comp_render = comp_tuple
			for pkg in comp_package.packages:
				comp_transform.server_position = math.Vector(**pkg['p'])
				comp_transform.server_velocity = math.Vector(**pkg['v'])
				if eid != self.world.master_eid():
					comp_transform.position = comp_transform.server_position
					comp_transform.velocity = comp_transform.server_velocity
				server_inter = comp_render.server_interpolation
				server_inter[0], server_inter[1] = server_inter[2], server_inter[3]
				server_inter[2], server_inter[3] = comp_transform.server_position, time.time()
