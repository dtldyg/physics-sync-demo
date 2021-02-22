# coding=utf-8

import base.const as const
import base.math as math
import base.ecs as ecs


class ComponentTransform(ecs.Component):
	def __init__(self, pos=math.vector_zero):
		super(ComponentTransform, self).__init__(ecs.LABEL_TRANSFORM)
		self.position = pos
		self.velocity = math.vector_zero
		if const.IS_CLIENT:
			self.server_position = pos
			self.server_velocity = math.vector_zero
