# coding=utf-8

import common.base.const as const
import common.physics as physics
import common.ec as ec


class CompPhysics(ec.ClientComponent):
	def __init__(self):
		super(CompPhysics, self).__init__('comp_physics')

	def update_logic(self, dt):
		if const.MASTER_PREDICT:
			comp_state = self.entity.get_comp('comp_state')
			comp_control = self.entity.get_comp('comp_control')
			comp_state.c_p, comp_state.c_v = physics.pv_with_force_normal(comp_state.c_p, comp_state.c_v, comp_control.f_nor, dt)

	def update_physics(self, dt):
		if const.MASTER_PREDICT:
			comp_state = self.entity.get_comp('comp_state')
			comp_state.c_p, comp_state.c_v = physics.pv_with_wall(comp_state.c_p, comp_state.c_v)

	# TODO 临时做法，重构为ecs
	def replay(self):
		comp_state = self.entity.get_comp('comp_state')
		comp_record = self.entity.get_comp('comp_record')
		for record in comp_record.records:
			p, v = physics.pv_with_force_normal(comp_state.s_p, comp_state.s_v, record['f'], record['dt'])
			comp_state.c_p, comp_state.c_v = physics.pv_with_wall(p, v)
