# coding=utf-8

import common.const as const
import common.math as math


class CompPhysics(object):
	def __init__(self, entity):
		self.entity = entity
		self.force = math.Vector()
		self.velocity = math.Vector()

	def update(self, dt):
		if self.force.zero() and self.velocity.zero():
			return

		# f = f - μ·mg·v_dir
		f = self.force - self.velocity.normal() * const.ENTITY_FRICTION * const.ENTITY_MASS * const.WORLD_G
		# a = f/m
		a = f / const.ENTITY_MASS
		# v = v0 + a·t
		v = self.velocity + a * dt
		if v.length() > const.ENTITY_MAX_V:
			v = v.normal() * const.ENTITY_MAX_V
		# s = v·t - similar to uniform motion
		s = v * dt

		to_v = v
		to_s = self.entity.pos + s
		# wall collision
		if to_s.x + const.ENTITY_RADIUS > const.SCREEN_SIZE[0]:
			to_v.x = -to_v.x
			to_s.x = const.ENTITY_RADIUS * 2 - const.SCREEN_SIZE[0] * 2 - to_s.x
		if to_s.y + const.ENTITY_RADIUS > const.SCREEN_SIZE[1]:
			to_v.y = -to_v.y
			to_s.y = const.ENTITY_RADIUS * 2 - const.SCREEN_SIZE[1] * 2 - to_s.y
		if to_s.x < const.ENTITY_RADIUS:
			to_v.x = -to_v.x
			to_s.x = const.ENTITY_RADIUS * 2 - to_s.x
		if to_s.y < const.ENTITY_RADIUS:
			to_v.y = -to_v.y
			to_s.y = const.ENTITY_RADIUS * 2 - to_s.y

		self.velocity = to_v
		self.entity.pos = to_s
