# coding=utf-8

import common.base.math as math
import ecs.component as component


class ComponentTransform(component.Component):
	def __init__(self, pos):
		super(ComponentTransform, self).__init__(component.LABEL_TRANSFORM)
		self.position = pos
		self.velocity = math.vector_zero
