# coding=utf-8

import common.math as math
import common.ec as ec


class CompState(ec.Component):
	def __init__(self):
		super(CompState, self).__init__('comp_state')
		self.velocity = math.Vector()
		self.pos = math.Vector()

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
