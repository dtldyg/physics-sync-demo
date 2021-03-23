# coding=utf-8

import base.ecs as ecs
import base.net as net
import base.const as const


class SystemExtrapolation(ecs.System):
	def __init__(self):
		super(SystemExtrapolation, self).__init__((ecs.LABEL_TRANSFORM,))

	def update(self, dt, component_tuples):
		master_eid = self.world.master_eid()
		for eid, comp_tuple in component_tuples:
			if eid == master_eid:
				continue
			if const.REPLICA_BEHAVIOR != const.REPLICA_EXTRAPOLATION and const.REPLICA_BEHAVIOR != const.REPLICA_PHYSIC_BLEND:
				continue
			# TODO 判断和master的距离，决定extrapolation_position进行外推还是使用server_position
			comp_transform, = comp_tuple
			extra_time = net.rtt[0] + (2 / const.LOGIC_FPS) + 1 / const.STATES_FPS
			comp_transform.extrapolation_velocity = comp_transform.server_velocity
			comp_transform.extrapolation_position = comp_transform.server_position + comp_transform.server_velocity * extra_time
