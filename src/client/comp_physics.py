# coding=utf-8

import common.const as const
import common.math as math
import common.ec as ec


class CompPhysics(ec.Component):
	def __init__(self):
		super(CompPhysics, self).__init__('comp_physics')
		self.force = math.Vector()

	def update_logic(self, dt):
		comp_state = self.entity.get_comp('comp_state')
		if self.force.zero() and comp_state.velocity.zero():
			return

		# --- 1.force analysis: Euler‘s Method ---
		# f = f - μ·mg·v_dir
		f = self.force - comp_state.velocity.normal() * const.ENTITY_FRICTION * const.ENTITY_MASS * const.WORLD_G
		# a = f/m
		a = f / const.ENTITY_MASS
		# v = v0 + a·t
		v = comp_state.velocity + a * dt
		if self.force.zero() and comp_state.velocity.length() <= a.length() * dt:
			# to zero
			v = math.Vector()
		if v.length() > const.ENTITY_MAX_V:
			# to max
			v = v.normal() * const.ENTITY_MAX_V
		# s = v·t - similar to uniform motion
		s = v * dt

		# --- 2.v/p update ---
		comp_state.velocity = v
		comp_state.pos = comp_state.pos + s

	def update_physics(self, dt):
		comp_state = self.entity.get_comp('comp_state')

		v = comp_state.velocity
		p = comp_state.pos

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
		# collision response(v swap)

		# --- 4.result show ---
		comp_state.velocity = v
		comp_state.pos = p
