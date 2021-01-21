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
		# v = v0 + a·t
		v = self.velocity + a * dt
		if v.length() > _const.ENTITY_MAX_V:
			v = v.normal() * _const.ENTITY_MAX_V
		# s = v·t
		s = v * dt

		self.velocity = v
		self.entity.pos = self.entity.pos + s
