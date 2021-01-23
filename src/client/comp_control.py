# coding=utf-8

import pygame
import client.window as window
import client.event as event
import common.const as const
import common.math as math
import common.switch as switch


class CompControl(object):
	def __init__(self, entity):
		self.entity = entity
		self.lining_stage = 0
		self.lining_start = None
		self.lining_end = None

	def update(self, _):
		self.entity.comp_physics.force = math.vector_zero
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
			if x != 0 or y != 0:
				force = math.Vector(x, y).normal() * const.ENTITY_FORCE
				self.entity.comp_physics.force = force
		elif switch.CONTROL_MODE == switch.CONTROL_MOUSE:
			if event.mouse_active():
				cur_pos = int(self.entity.comp_state.pos.x), int(self.entity.comp_state.pos.y)
				mouse_pos = pygame.mouse.get_pos()
				if mouse_pos[0] - cur_pos[0] != 0 or mouse_pos[1] - cur_pos[1] != 0:
					force = (math.Vector(*mouse_pos) - math.Vector(*cur_pos)).normal() * const.ENTITY_FORCE
					self.entity.comp_physics.force = force
		elif switch.CONTROL_MODE == switch.CONTROL_LINE:
			cur_pos = self.entity.comp_state.pos
			mouse_pos = pygame.mouse.get_pos()
			# update line
			if self.lining_stage == 1:
				self.lining_start = cur_pos
				self.lining_end = mouse_pos
			if event.mouse_trigger_down(1):
				# line begin
				if (math.Vector(*mouse_pos) - cur_pos).length() < const.ENTITY_RADIUS:
					self.lining_stage = 1
					self.lining_start = cur_pos
					self.lining_end = mouse_pos
				# line cancel
				else:
					self.line_reset()
			if self.lining_stage == 1 and event.mouse_trigger_up(1):
				# line end
				self.lining_stage = 2
			if self.lining_stage == 2 and event.mouse_trigger_up(3):
				# line trigger
				v_dir = math.Vector(*self.lining_end) - self.lining_start
				v_len = v_dir.length()
				if v_len > const.CONTROL_LINE_RADIUS:
					v_len = const.CONTROL_LINE_RADIUS
				self.entity.comp_physics.velocity = v_dir.normal() * const.ENTITY_MAX_V * (v_len / const.CONTROL_LINE_RADIUS)
				# line over
				self.line_reset()
			# draw line
			if self.lining_stage == 1 or self.lining_stage == 2:
				args_line = window.screen, const.CONTROL_LINE_COLOR, self.lining_start.tuple(), self.lining_end
				self.entity.comp_render.others.append((pygame.draw.aaline, args_line))
				args_circle = window.screen, const.CONTROL_LINE_COLOR, self.lining_start.tuple(), const.CONTROL_LINE_RADIUS, const.CONTROL_LINE_WIDTH
				self.entity.comp_render.others.append((pygame.draw.circle, args_circle))

	def sync_out(self):
		pass

	def sync_in(self, pkg):
		pass

	def line_reset(self):
		self.lining_stage = 0
		self.lining_start = None
		self.lining_end = None
