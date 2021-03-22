# coding=utf-8

import base.math as math
import base.ecs as ecs
import base.const as const


class SystemRecvState(ecs.System):
	def __init__(self):
		super(SystemRecvState, self).__init__((ecs.LABEL_PACKAGE, ecs.LABEL_TRANSFORM))

	def update(self, dt, component_tuples):
		master_eid = self.world.master_eid()
		for eid, comp_tuple in component_tuples:
			comp_package, comp_transform = comp_tuple
			for pkg in comp_package.packages:
				comp_transform.server_position = math.Vector(**pkg['p'])
				comp_transform.server_velocity = math.Vector(**pkg['v'])
				comp_transform.server_modified = True
				if (eid == master_eid and const.MASTER_BEHAVIOR == const.MASTER_NONE) or (eid != master_eid and const.REPLICA_BEHAVIOR == const.REPLICA_NONE):
					comp_transform.position = comp_transform.server_position
					comp_transform.velocity = comp_transform.server_velocity
					comp_transform.modified = True
