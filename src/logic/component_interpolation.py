# coding=utf-8

import base.ecs as ecs


class ComponentInterpolation(ecs.Component):
	def __init__(self):
		super(ComponentInterpolation, self).__init__(ecs.LABEL_INTERPOLATION)
		self.mode = None
		self.pass_t = 0
		self.remain_t = 0
		self.cubic_args = [0] * 4
