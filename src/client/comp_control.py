# coding=utf-8

import pygame
import client.event as event
import common.const as const
import common.math as math


class CompControl(object):
	def __init__(self, entity):
		self.entity = entity

	def update(self, _):
		x, y = 0, 0
		if event.key_state(pygame.K_w):
			y = -1
		if event.key_state(pygame.K_s):
			y = 1
		if event.key_state(pygame.K_a):
			x = -1
		if event.key_state(pygame.K_d):
			x = 1
		if x == 0 and y == 0:
			force = math.vector_zero
		else:
			force = math.Vector(x, y).normal() * const.ENTITY_FORCE
		self.entity.comp_physics.force = force
