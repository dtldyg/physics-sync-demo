# coding=utf-8

import common.base.math as math
import ecs.component as component


class CompControl(component.Component):
	def __init__(self):
		super(CompControl, self).__init__('component_control')
		self.f_nor = math.vector_zero
