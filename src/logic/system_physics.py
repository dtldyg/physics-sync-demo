# coding=utf-8

import base.const as const
import base.math as math
import base.ecs as ecs


class SystemPhysics(ecs.System):
	def __init__(self):
		super(SystemPhysics, self).__init__((ecs.LABEL_PHYSICS, ecs.LABEL_TRANSFORM))
		self.roll_forward = True

	def update(self, dt, component_tuples):
		# move
		for _, comp_tuple in component_tuples:
			comp_physics, comp_transform = comp_tuple
			f_nor = comp_physics.force_normal
			p, v = comp_transform.position, comp_transform.velocity
			if f_nor.zero() and v.zero():
				return p, v
			# --- 1.force analysis: Euler‘s Method ---
			# f = f - μ·mg·v_dir
			f_join = f_nor * const.ENTITY_FORCE - v.normal() * const.ENTITY_FRICTION * const.ENTITY_MASS * const.WORLD_G
			# a = f/m
			a = f_join / const.ENTITY_MASS
			# v = v0 + a·t
			v = v + a * dt
			if f_nor.zero() and v.length() <= a.length() * dt:
				# to zero
				v = math.vector_zero
			if v.length() > const.ENTITY_MAX_V:
				# to max
				v = v.normal() * const.ENTITY_MAX_V
			# s = v·t - similar to uniform motion
			s = v * dt
			# --- 2.v/p update ---
			comp_transform.position = p + s
			comp_transform.velocity = v
		# collision
		for _, comp_tuple in component_tuples:
			_, comp_transform = comp_tuple
			p, v = comp_transform.position, comp_transform.velocity
			# --- 3.collision check ---
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
			# --- 4.result show ---
			comp_transform.position = p
			comp_transform.velocity = v
