# coding=utf-8

import common.base.math as math
import common.ec as ec


class CompState(ec.ClientComponent):
	def __init__(self):
		super(CompState, self).__init__('comp_state')
		self.is_init = False
		self.c_v = math.vector_zero
		self.c_p = math.vector_zero
		self.s_v = math.vector_zero
		self.s_p = math.vector_zero

	def recv_state(self, state):
		self.s_p = math.Vector(**state['p'])
		self.s_v = math.Vector(**state['v'])
		# TODO 直接通过回滚设置，physics也不要在没开预测时跑，开了后依赖回滚更正
		if not self.is_init:
			self.is_init = True
			self.c_p = self.s_p
			self.c_v = self.s_v
