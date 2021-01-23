# coding=utf-8

import pygame
import client.event as event
import common.const as const
import common.math as math
import common.switch as switch


class CompControl(object):
	def __init__(self, entity):
		self.entity = entity

	def update(self, _):
		if switch.CONTROL_MODE == switch.CONTROL_WASD:
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
				force_dir = math.vector_zero
			else:
				force_dir = math.Vector(x, y)
		elif switch.CONTROL_MODE == switch.CONTROL_MOUSE:
			if not event.mouse_active():
				force_dir = math.vector_zero
			else:
				mouse_pos = pygame.mouse.get_pos()
				cur_pos = int(self.entity.comp_state.pos.x), int(self.entity.comp_state.pos.y)
				force_dir = math.Vector(*mouse_pos) - math.Vector(*cur_pos)
		else:
			force_dir = math.vector_zero
		force = force_dir.normal() * const.ENTITY_FORCE
		self.entity.comp_physics.force = force

	def sync_out(self):
		pass

	def sync_in(self, pkg):
		pass
