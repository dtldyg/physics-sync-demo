# coding=utf-8

import common.base.math as math
import common.base.const as const
import common.ec as ec


class CompState(ec.ClientComponent):
	def __init__(self):
		super(CompState, self).__init__('comp_state')
		self.is_init = False
		self.c_p = math.vector_zero
		self.c_v = math.vector_zero
		self.s_p = math.vector_zero
		self.s_v = math.vector_zero

	def recv_state(self, state):
		self.s_p = math.Vector(**state['p'])
		self.s_v = math.Vector(**state['v'])
		if not const.MASTER_PREDICT or not self.is_init:
			self.is_init = True
			self.c_p = self.s_p
			self.c_v = self.s_v
