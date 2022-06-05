# coding=utf-8

import base.ecs as ecs
import base.net as net
import base.const as const


class SystemExtrapolation(ecs.System):
	def __init__(self, world):
		super(SystemExtrapolation, self).__init__(world, (ecs.LABEL_TRANSFORM, ecs.LABEL_EXTRAPOLATION))
		self.roll_forward = True

	def update(self, dt, component_tuples):
		if const.REPLICA_BEHAVIOR != const.REPLICA_EXTRAPOLATION and const.REPLICA_BEHAVIOR != const.REPLICA_PHYSIC_BLEND:
			return
		for eid, comp_tuple in component_tuples:
			comp_transform, comp_polation = comp_tuple
			need_extra = True  # TODO 遍历其他entity判断碰撞范围内才需要外插
			if need_extra:
				extra_time = net.rtt[0] + (2 / const.LOGIC_FPS) + 1 / const.STATES_FPS
				comp_polation.extra_velocity = comp_transform.server_velocity
				comp_polation.extra_position = comp_transform.server_position + comp_transform.server_velocity * extra_time
			else:
				comp_polation.extra_velocity = comp_transform.server_velocity
				comp_polation.extra_position = comp_transform.server_position
