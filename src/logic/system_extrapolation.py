# coding=utf-8

import base.ecs as ecs
import base.net as net
import base.const as const


class SystemExtrapolation(ecs.System):
	def __init__(self):
		super(SystemExtrapolation, self).__init__((ecs.LABEL_TRANSFORM,))
		self.roll_forward = True

	def update(self, dt, component_tuples):
		master_eid = self.world.master_eid()
		master_comp_transform = self.world.master_component(ecs.LABEL_TRANSFORM) if master_eid > 0 else None
		for eid, comp_tuple in component_tuples:
			if eid == master_eid:
				continue
			if const.REPLICA_BEHAVIOR != const.REPLICA_EXTRAPOLATION and const.REPLICA_BEHAVIOR != const.REPLICA_PHYSIC_BLEND:
				continue
			comp_transform, = comp_tuple
			need_extra = True
			if const.REPLICA_BEHAVIOR == const.REPLICA_PHYSIC_BLEND:
				if master_comp_transform is None or (master_comp_transform.position - comp_transform.position).length_sqr() > const.EXTRAPOLATION_AOI_SQR:
					need_extra = False
			if need_extra:
				extra_time = net.rtt[0] + (2 / const.LOGIC_FPS) + 1 / const.STATES_FPS
				comp_transform.extrapolation_velocity = comp_transform.server_velocity
				comp_transform.extrapolation_position = comp_transform.server_position + comp_transform.server_velocity * extra_time
			else:
				comp_transform.extrapolation_velocity = comp_transform.server_velocity
				comp_transform.extrapolation_position = comp_transform.server_position
