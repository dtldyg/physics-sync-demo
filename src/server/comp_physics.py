# coding=utf-8

import common.math as math


class CompPhysics(object):
	def __init__(self, entity):
		self.entity = entity
		self.velocity = math.Vector()

	def update(self, _):
		pass
