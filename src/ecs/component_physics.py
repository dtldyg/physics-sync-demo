# coding=utf-8

import common.base.math as math
import ecs.component as component


class ComponentPhysics(component.Component):
	def __init__(self):
		super(ComponentPhysics, self).__init__(component.LABEL_PHYSICS)
		self.force_normal = math.vector_zero
