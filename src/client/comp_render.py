# coding=utf-8

import pygame
import client.game as game


class CompRender(object):
	def __init__(self, entity):
		self.entity = entity

	def update(self, _):
		pygame.draw.circle(game.screen, self.entity.color, self.entity.pos.tuple(), self.entity.radius)
