# coding=utf-8

import common.base.math as math
import common.base.const as const
import ecs.component as component


class ComponentTransform(component.Component):
	def __init__(self):
		super(ComponentTransform, self).__init__(component.LABEL_TRANSFORM)
		self.position = math.Vector(*const.MASTER_INIT_POS)
		self.velocity = math.vector_zero
