# coding=utf-8

import pygame
import client.window as window
import common.const as const
import common.math as math
import common.switch as switch


class CompRender(object):
	def __init__(self, entity):
		self.entity = entity
		self.surface = self.entity_surface()
		self.others = []

	def update(self, _):
		if self.entity.is_master and not self.entity.is_shadow and not switch.MASTER_PREDICT:
			return
		window.screen.blit(self.surface[0], (self.entity.comp_state.pos - self.surface[1]).tuple())
		for other in self.others:
			other[0](*other[1])
		self.others.clear()

	def sync_out(self):
		pass

	def sync_in(self, pkg):
		pass

	def entity_surface(self):
		if self.entity.is_master:
			color = const.MASTER_SHADOW_COLOR if self.entity.is_shadow else const.MASTER_COLOR
		else:
			color = const.REPLICA_SHADOW_COLOR if self.entity.is_shadow else const.REPLICA_COLOR
		radius = const.ENTITY_RADIUS
		surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
		pygame.draw.circle(surface, color, (radius, radius), radius)
		offset = math.Vector(radius, radius)
		return surface, offset
