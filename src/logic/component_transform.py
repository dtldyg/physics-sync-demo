# coding=utf-8

import base.const as const
import base.math as math
import base.ecs as ecs


class ComponentTransform(ecs.Component):
	def __init__(self, pos=math.vector_zero, is_master=False):
		super(ComponentTransform, self).__init__(ecs.LABEL_TRANSFORM)
		self.position = pos
		self.velocity = math.vector_zero
		self.modified = True
		if const.IS_CLIENT:
			self.server_position = pos
			self.server_velocity = math.vector_zero
			self.server_modified = True
			if not is_master:
				self.extrapolation_position = pos
				self.extrapolation_velocity = math.vector_zero
				self.interpolation_position = pos
				self.interpolation_velocity = math.vector_zero
