# coding=utf-8

import base.math as math
import base.ecs as ecs


class ComponentExtrapolation(ecs.Component):
	def __init__(self, pos=math.vector_zero):
		super(ComponentExtrapolation, self).__init__(ecs.LABEL_EXTRAPOLATION)
		self.extra_position = pos
		self.extra_velocity = math.vector_zero
