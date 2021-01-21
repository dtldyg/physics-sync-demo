# coding=utf-8

import _math
import _const


class CompPhysics(object):
	def __init__(self, entity):
		self.entity = entity
		self.force = _math.Vector()
		self.velocity = _math.Vector()

	def update(self, dt):
		if self.force.zero() and self.velocity.zero():
			return
		# f = f - μ·mg·v_dir
		f = self.force - self.velocity.normal() * _const.ENTITY_FRICTION * _const.ENTITY_MASS * _const.WORLD_G
		# a = f/m
		a = f / _const.ENTITY_MASS
		# v = v0 + at
		v = self.velocity + a * dt
		# s = v0t + 1/2at2
		s = self.velocity + a * 0.5 * (dt ** 2)
		self.velocity = v
		self.entity.pos = self.entity.pos + s
