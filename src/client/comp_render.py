# coding=utf-8

import time
import pygame

import common.base.const as const
import common.base.math as math
import common.ec as ec


class CompRender(ec.ClientComponent):
	def __init__(self):
		super(CompRender, self).__init__('comp_render')
		# client entity
		c_sur = pygame.Surface((const.ENTITY_RADIUS * 2, const.ENTITY_RADIUS * 2), pygame.SRCALPHA)
		pygame.draw.circle(c_sur, const.MASTER_CLIENT_COLOR, (const.ENTITY_RADIUS, const.ENTITY_RADIUS), const.ENTITY_RADIUS)
		self.c_en_sur = (c_sur, math.Vector(const.ENTITY_RADIUS, const.ENTITY_RADIUS))  # client local
		self.c_en_a_p = None
		self.c_en_a_t = None
		self.c_en_b_p = None
		self.c_en_b_t = None
		# server entity
		s_sur = pygame.Surface((const.ENTITY_RADIUS * 2, const.ENTITY_RADIUS * 2), pygame.SRCALPHA)
		pygame.draw.circle(s_sur, const.MASTER_SERVER_COLOR, (const.ENTITY_RADIUS, const.ENTITY_RADIUS), const.ENTITY_RADIUS)
		self.s_en_sur = (s_sur, math.Vector(const.ENTITY_RADIUS, const.ENTITY_RADIUS))  # server remote
		# others
		self.others = []

	def update_logic(self, _):
		self.others.clear()
		self.c_en_a_p, self.c_en_a_t = self.c_en_b_p, self.c_en_b_t
		self.c_en_b_p, self.c_en_b_t = self.entity.get_comp('comp_state').c_p, time.time()

	def update_render(self, sur, _):
		comp_state = self.entity.get_comp('comp_state')
		if const.MASTER_PREDICT:
			sur.blit(self.c_en_sur[0], (self.render_interpolation_c_p() - self.c_en_sur[1]).tuple())
			if const.MASTER_PREDICT_SERVER:
				sur.blit(self.s_en_sur[0], (comp_state.s_p - self.s_en_sur[1]).tuple())
		else:
			sur.blit(self.c_en_sur[0], (self.render_interpolation_c_p() - self.c_en_sur[1]).tuple())
		for other in self.others:
			other[0](sur, *other[1])

	def render_interpolation_c_p(self):
		if self.c_en_a_p is None:
			return self.c_en_b_p
		t = time.time() - self.c_en_b_t
		if t >= self.c_en_b_t - self.c_en_a_t:
			return self.c_en_b_p
		return (self.c_en_b_p - self.c_en_a_p) * t / (self.c_en_b_t - self.c_en_a_t) + self.c_en_a_p

	def add_render(self, r_func, r_arg):
		self.others.append((r_func, r_arg))
