# coding=utf-8

import pygame
import client.window as window
import common.const as const
import common.math as math


class CompRender(object):
	def __init__(self, entity):
		self.entity = entity
		if self.entity.is_master:
			if self.entity.is_shadow:
				self.color = const.MASTER_SHADOW_COLOR
			else:
				self.color = const.MASTER_COLOR
		self.radius = const.ENTITY_RADIUS
		self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
		pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)
		self.offset = math.Vector(self.radius, self.radius)

	def update(self, _):
		window.screen.blit(self.surface, (self.entity.comp_state.pos - self.offset).tuple())
