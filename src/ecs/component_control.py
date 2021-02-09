# coding=utf-8

import common.base.math as math
import ecs.component as component


class ComponentControl(component.Component):
	def __init__(self):
		super(ComponentControl, self).__init__(component.LABEL_CONTROL)
		self.force_normal = math.vector_zero
