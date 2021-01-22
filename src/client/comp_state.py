# coding=utf-8

import common.const as const
import common.math as math


class CompState(object):
	def __init__(self, entity):
		self.entity = entity
		if entity.is_master:
			self.pos = math.Vector(*const.MASTER_INIT_POS)

	def update(self, _):
		print(self.pos.tuple())
