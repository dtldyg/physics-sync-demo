# coding=utf-8

import pygame
import _input
import _math
import _const


class CompControl(object):
	def __init__(self, entity):
		self.entity = entity

	def update(self, _):
		x, y = 0, 0
		if _input.key_state(pygame.K_w):
			y = -1
		if _input.key_state(pygame.K_s):
			y = 1
		if _input.key_state(pygame.K_a):
			x = -1
		if _input.key_state(pygame.K_d):
			x = 1
		if x == 0 and y == 0:
			force = _math.vector_zero
		else:
			force = _math.Vector(x, y).normal() * _const.ENTITY_FORCE
		self.entity.comp_physics.force = force
