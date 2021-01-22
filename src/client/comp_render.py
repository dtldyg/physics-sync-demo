# coding=utf-8

import pygame
import client.game as game
import common.const as const


class CompRender(object):
	def __init__(self, entity):
		self.entity = entity
		if self.entity.is_master:
			self.color = const.MASTER_COLOR
			self.radius = const.ENTITY_RADIUS

	def update(self, _):
		pygame.draw.circle(game.screen, self.color, self.entity.comp_state.pos.tuple(), self.radius)
