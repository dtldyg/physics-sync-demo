# coding=utf-8

import common.physics as physics
import common.ec as ec


class CompPhysics(ec.ServerComponent):
	def __init__(self):
		super(CompPhysics, self).__init__('comp_physics')

	def update_logic(self, dt):
		comp_state = self.entity.get_comp('comp_state')
		comp_control = self.entity.get_comp('comp_control')
		comp_state.p, comp_state.v = physics.pv_with_force_normal(comp_state.p, comp_state.v, comp_control.f_nor, dt)

	def update_physics(self, dt):
		comp_state = self.entity.get_comp('comp_state')
		comp_state.p, comp_state.v = physics.pv_with_wall(comp_state.p, comp_state.v)
