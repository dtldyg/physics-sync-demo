# coding=utf-8

import common.base.math as math
import common.ec as ec


class CompState(ec.ClientComponent):
	def __init__(self):
		super(CompState, self).__init__('comp_state')
		self.v = math.vector_zero
		self.p = math.vector_zero

	def recv_state(self, state):
		self.p = math.Vector(**state['p'])
		self.v = math.Vector(**state['v'])
