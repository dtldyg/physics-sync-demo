# coding=utf-8

import common.base.const as const
import common.base.math as math
import ecs.component as component


class ComponentTransform(component.Component):
	def __init__(self, pos=math.vector_zero):
		super(ComponentTransform, self).__init__(component.LABEL_TRANSFORM)
		self.position = pos
		self.velocity = math.vector_zero
		if const.IS_CLIENT:
			self.server_position = math.vector_zero
			self.server_velocity = math.vector_zero
