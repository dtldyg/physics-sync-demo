# coding=utf-8

import common.base.math as math
import common.ec as ec


class CompState(ec.ServerComponent):
	def __init__(self):
		super(CompState, self).__init__('comp_state')
		self.dirty = False
		self.p = math.Vector()
		self.v = math.Vector()

	def send_state(self, state):
		state['p'] = self.p.__dict__
		state['v'] = self.p.__dict__
