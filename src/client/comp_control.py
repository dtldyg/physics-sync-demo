# coding=utf-8

import pygame

import common.base.const as const
import common.base.math as math
import common.base.switch as switch
import common.ec as ec

import client.event as event
import client.display.surface as window


class CompControl(ec.Component):
	def __init__(self):
		super(CompControl, self).__init__('comp_control')
		self.line_stage = 0  # 0:none 1:draw 2:wait 3:trigger
		self.line_start = None
		self.line_end = None
		self.line_f_dir = None
		self.line_t = 0

	def update_logic(self, dt):
		comp_physics = self.entity.get_comp('comp_physics')
		comp_state = self.entity.get_comp('comp_state')
		comp_render = self.entity.get_comp('comp_render')

		comp_physics.f = math.vector_zero
		# wasd
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
				comp_physics.f = force
		# follow mouse
		elif switch.CONTROL_MODE == switch.CONTROL_MOUSE:
			if event.mouse_active() and event.key_state(pygame.K_SPACE):
				cur_pos = int(comp_state.pos.x), int(comp_state.pos.y)
				mouse_pos = pygame.mouse.get_pos()
				if mouse_pos[0] - cur_pos[0] != 0 or mouse_pos[1] - cur_pos[1] != 0:
					force = (math.Vector(*mouse_pos) - math.Vector(*cur_pos)).normal() * const.ENTITY_FORCE
					comp_physics.f = force
		# archery
		elif switch.CONTROL_MODE == switch.CONTROL_LINE:
			cur_pos = comp_state.pos
			mouse_pos = pygame.mouse.get_pos()
			if event.mouse_trigger_down(1) and not self.line_stage == 3:
				# line begin draw
				if (math.Vector(*mouse_pos) - cur_pos).length() < const.ENTITY_RADIUS:
					self.line_stage = 1
					self.line_start = cur_pos
					self.line_end = mouse_pos
				# line over
				else:
					self.line_reset()
			# line drawing
			if self.line_stage == 1:
				self.line_start = cur_pos
				self.line_end = mouse_pos
			# line draw over
			if self.line_stage == 1 and event.mouse_trigger_up(1):
				self.line_stage = 2
			# line begin trigger
			if self.line_stage == 2 and event.mouse_trigger_up(3):
				f_dir = math.Vector(*self.line_end) - self.line_start
				f_k = f_dir.length() / const.CONTROL_LINE_RADIUS
				self.line_f_dir = f_dir.normal()
				self.line_t = const.CONTROL_LINE_TIME * f_k if f_k < 1 else const.CONTROL_LINE_TIME
				self.line_stage = 3
			# line triggering
			if self.line_stage == 3:
				if self.line_t > 0:
					force = self.line_f_dir * const.ENTITY_FORCE
					comp_physics.f = force
					self.line_t = self.line_t - dt
				else:
					# line trigger over
					self.line_reset()
			# draw line
			if self.line_stage == 1 or self.line_stage == 2:
				args_line = window.sur_game, const.CONTROL_LINE_COLOR, self.line_start.tuple(), self.line_end
				comp_render.others.append((pygame.draw.aaline, args_line))
				if self.line_stage == 1:
					args_circle = window.sur_game, const.CONTROL_LINE_COLOR, self.line_start.tuple(), const.CONTROL_LINE_RADIUS, const.CONTROL_LINE_WIDTH
					comp_render.others.append((pygame.draw.circle, args_circle))

	def line_reset(self):
		self.line_stage = 0
		self.line_start = None
		self.line_end = None
		self.line_f_dir = 0
		self.line_t = 0
