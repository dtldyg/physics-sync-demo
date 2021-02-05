# coding=utf-8

import common.base.const as const
import common.base.math as math
import server.entity as ec


class CompPhysics(ec.ServerComponent):
	def __init__(self):
		super(CompPhysics, self).__init__('comp_physics')
		self.f = math.Vector()

	def update_logic(self, dt):
		comp_state = self.entity.get_comp('comp_state')
		if self.f.zero() and comp_state.v.zero():
			return

		# --- 1.force analysis: Euler‘s Method ---
		# f = f - μ·mg·v_dir
		f = self.f - comp_state.v.normal() * const.ENTITY_FRICTION * const.ENTITY_MASS * const.WORLD_G
		# a = f/m
		a = f / const.ENTITY_MASS
		# v = v0 + a·t
		v = comp_state.v + a * dt
		if self.f.zero() and comp_state.v.length() <= a.length() * dt:
			# to zero
			v = math.Vector()
		if v.length() > const.ENTITY_MAX_V:
			# to max
			v = v.normal() * const.ENTITY_MAX_V
		# s = v·t - similar to uniform motion
		s = v * dt

		# --- 2.v/p update ---
		comp_state.p = comp_state.p + s
		comp_state.v = v

	def update_physics(self, dt):
		comp_state = self.entity.get_comp('comp_state')

		p = comp_state.p
		v = comp_state.v

		# --- 3.collision check ---
		# wall collision
		if p.x + const.ENTITY_RADIUS > const.SCREEN_SIZE[0]:
			v.x = -v.x
			p.x = const.SCREEN_SIZE[0] * 2 - const.ENTITY_RADIUS * 2 - p.x
		if p.y + const.ENTITY_RADIUS > const.SCREEN_SIZE[1]:
			v.y = -v.y
			p.y = const.SCREEN_SIZE[1] * 2 - const.ENTITY_RADIUS * 2 - p.y
		if p.x < const.ENTITY_RADIUS:
			v.x = -v.x
			p.x = const.ENTITY_RADIUS * 2 - p.x
		if p.y < const.ENTITY_RADIUS:
			v.y = -v.y
			p.y = const.ENTITY_RADIUS * 2 - p.y
		# entity collision

		# --- 4.result show ---
		comp_state.p = p
		comp_state.v = v
