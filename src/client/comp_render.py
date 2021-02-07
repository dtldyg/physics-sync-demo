# coding=utf-8

import pygame

import common.base.const as const
import common.base.math as math
import common.ec as ec


class CompRender(ec.ClientComponent):
	def __init__(self):
		super(CompRender, self).__init__('comp_render')
		surface = pygame.Surface((const.ENTITY_RADIUS * 2, const.ENTITY_RADIUS * 2), pygame.SRCALPHA)
		pygame.draw.circle(surface, const.MASTER_COLOR, (const.ENTITY_RADIUS, const.ENTITY_RADIUS), const.ENTITY_RADIUS)
		self.entity_sur = (surface, math.Vector(const.ENTITY_RADIUS, const.ENTITY_RADIUS))
		self.others = []

	def update_logic(self, _):
		self.others.clear()

	def update_render(self, sur, _):
		sur.blit(self.entity_sur[0], (self.entity.get_comp('comp_state').p - self.entity_sur[1]).tuple())
		for other in self.others:
			other[0](sur, *other[1])

	def add_render(self, r_func, r_arg):
		self.others.append((r_func, r_arg))
