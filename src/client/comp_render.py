# coding=utf-8

import pygame

import common.base.const as const
import common.base.math as math
import common.base.ec as ec

import client.ui.window as window


class CompRender(ec.Component):
	def __init__(self):
		super(CompRender, self).__init__('comp_render')
		self.surface = None
		self.others = []

	def init(self):
		self.surface = self.entity_surface()

	def update_render(self, _):
		if self.entity.has_flags(const.ENTITY_FLAG_MASTER, const.ENTITY_FLAG_LOCAL) is False or const.MASTER_PREDICT:
			window.screen.blit(self.surface[0], (self.entity.get_comp('comp_state').pos - self.surface[1]).tuple())
		for other in self.others:
			other[0](*other[1])
		self.others.clear()

	def entity_surface(self):
		if self.entity.has_flags(const.ENTITY_FLAG_MASTER):
			color = const.MASTER_SHADOW_COLOR if self.entity.has_flags(const.ENTITY_FLAG_SHADOW) else const.MASTER_COLOR
		else:
			color = const.REPLICA_SHADOW_COLOR if self.entity.has_flags(const.ENTITY_FLAG_SHADOW) else const.REPLICA_COLOR
		radius = const.ENTITY_RADIUS
		surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
		pygame.draw.circle(surface, color, (radius, radius), radius)
		offset = math.Vector(radius, radius)
		return surface, offset
