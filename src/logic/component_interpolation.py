# coding=utf-8

import base.math as math
import base.ecs as ecs


class ComponentInterpolation(ecs.Component):
	def __init__(self, pos=math.vector_zero):
		super(ComponentInterpolation, self).__init__(ecs.LABEL_INTERPOLATION)
		self.mode = None
		self.pass_t = 0
		self.remain_t = 0
		self.cubic_args = [0] * 4
		self.inter_position = pos
		self.inter_velocity = math.vector_zero
