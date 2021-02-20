# coding=utf-8

import base.math as math
import base.ecs as ecs


class ComponentPhysics(ecs.Component):
	def __init__(self):
		super(ComponentPhysics, self).__init__(ecs.LABEL_PHYSICS)
		self.force_normal = math.vector_zero
