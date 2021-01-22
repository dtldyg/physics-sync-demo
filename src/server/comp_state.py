# coding=utf-8

import common.const as const
import common.math as math


class CompState(object):
	def __init__(self, entity):
		self.entity = entity
		self.pos = None

	def update(self, _):
		pass
