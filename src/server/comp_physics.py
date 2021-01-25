# coding=utf-8

import common.ec as ec


class CompPhysics(ec.Component):
	def __init__(self):
		super(CompPhysics, self).__init__('comp_physics')

	def init(self):
		pass

	def io_in(self, pkg):
		pass

	def update_logic(self, dt):
		pass

	def update_physics(self, dt):
		pass

	def update_render(self, dt):
		pass

	def io_out(self):
		pass
