# coding=utf-8

import base.math as math
import base.ecs as ecs
import base.const as const


class ComponentPhysics(ecs.Component):
	def __init__(self, is_master=False):
		super(ComponentPhysics, self).__init__(ecs.LABEL_PHYSICS)
		self._force_normal_fixed = math.vector_zero
		if const.IS_CLIENT:
			if not is_master:
				self.blending = False
				self.blend_time = 0
		else:
			self._dt_fixed = 0

	# --- ensure use fixed-point number in c/s sync ---
	@property
	def dt_fixed(self):
		return self._dt_fixed

	@dt_fixed.setter
	def dt_fixed(self, value):
		self._dt_fixed = value

	@property
	def dt(self):
		return self._dt_fixed / 1e9

	@dt.setter
	def dt(self, value):
		self._dt_fixed = int(value * 1e9)

	@property
	def force_normal_fixed(self):
		return self._force_normal_fixed

	@force_normal_fixed.setter
	def force_normal_fixed(self, value):
		self._force_normal_fixed = value

	@property
	def force_normal(self):
		if self._force_normal_fixed is None:
			return None
		return self._force_normal_fixed.to_float()

	@force_normal.setter
	def force_normal(self, value):
		if value is None:
			self._force_normal_fixed = None
		else:
			self._force_normal_fixed = value.to_fixed()
