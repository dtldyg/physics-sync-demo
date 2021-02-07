# coding=utf-8

import common.base.math as math
import common.base.const as const
import common.ec as ec


class CompState(ec.ServerComponent):
	def __init__(self):
		super(CompState, self).__init__('comp_state')
		self.p = math.Vector(*const.MASTER_INIT_POS)
		self.v = math.vector_zero

	def send_state(self, state):
		state['fr'] = self.entity.frame
		state['p'] = self.p.__dict__
		state['v'] = self.v.__dict__
