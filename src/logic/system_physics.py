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
		last_position = {}
		for eid, comp_tuple in component_tuples:
			comp_physics, comp_transform = comp_tuple
			last_position[eid] = comp_transform.position
			f_nor = comp_physics.force_normal
			p, v = comp_transform.position, comp_transform.velocity
			if f_nor.zero() and v.zero():
				continue
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
			comp_transform.position = p + s
			comp_transform.velocity = v
			comp_transform.modified = True
		# collision
		# --- with others
		manifolds = {}
		for i in range(len(component_tuples)):
			for j in range(i + 1, len(component_tuples)):
				trans_a = component_tuples[i][1][1]
				trans_b = component_tuples[j][1][1]
				p_ab = trans_b.position - trans_a.position
				if p_ab.length_sqr < (const.ENTITY_RADIUS * 2) ** 2:
					if trans_a not in manifolds:
						manifolds[trans_a] = [math.vector_zero, math.vector_zero]  # position_fix, impulse_fix
					if trans_b not in manifolds:
						manifolds[trans_b] = [math.vector_zero, math.vector_zero]
					n_b = p_ab.normal()
					n_a = -n_b
					p_fix = const.ENTITY_RADIUS - p_ab.length / 2
					# position fix
					manifolds[trans_a][0] += n_a * p_fix
					manifolds[trans_b][0] += n_b * p_fix
					# velocity fix https://github.com/phenomLi/Blog/issues/35
					e = const.ENTITY_RESTITUTION
					p_ab = trans_b.velocity - trans_a.velocity
					j = -(1 + e) * p_ab.dot(n_a) / (1 / const.ENTITY_MASS * 2)
					manifolds[trans_a][1] += n_a * j
					manifolds[trans_b][1] += n_b * j
		for comp_transform, fix in manifolds.items():
			comp_transform.position += fix[0]
			comp_transform.velocity += fix[1] / const.ENTITY_MASS
			comp_transform.modified = True
		# --- with wall
		for _, comp_tuple in component_tuples:
			_, comp_transform = comp_tuple
			p, v = comp_transform.position, comp_transform.velocity
			collide = False
			if p.x + const.ENTITY_RADIUS > const.SCREEN_SIZE[0]:
				v.x = -v.x
				p.x = const.SCREEN_SIZE[0] * 2 - const.ENTITY_RADIUS * 2 - p.x
				collide = True
			if p.y + const.ENTITY_RADIUS > const.SCREEN_SIZE[1]:
				v.y = -v.y
				p.y = const.SCREEN_SIZE[1] * 2 - const.ENTITY_RADIUS * 2 - p.y
				collide = True
			if p.x < const.ENTITY_RADIUS:
				v.x = -v.x
				p.x = const.ENTITY_RADIUS * 2 - p.x
				collide = True
			if p.y < const.ENTITY_RADIUS:
				v.y = -v.y
				p.y = const.ENTITY_RADIUS * 2 - p.y
				collide = True
			if collide:
				comp_transform.position = p
				comp_transform.velocity = v
				comp_transform.modified = True
