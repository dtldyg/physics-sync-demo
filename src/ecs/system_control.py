# coding=utf-8

import pygame
import common.base.const as const
import common.base.math as math
import ecs.system as system
import ecs.component as component


class SystemControl(system.System):
	def __init__(self):
		super(SystemControl, self).__init__((component.LABEL_INPUT, component.LABEL_CONTROL, component.LABEL_PHYSICS, component.LABEL_TRANSFORM))

	def update(self, dt, component_tuples):
		for _, component_tuple in component_tuples:
			component_input, component_control, component_physics, component_transform = component_tuple
			component_physics.force_normal = math.vector_zero

			# wasd
			if const.CONTROL_MODE == const.CONTROL_WASD:
				x, y = 0, 0
				if pygame.K_w in component_input.key_down:
					y = -1
				if pygame.K_s in component_input.key_down:
					y = 1
				if pygame.K_a in component_input.key_down:
					x = -1
				if pygame.K_d in component_input.key_down:
					x = 1
				if x != 0 or y != 0:
					component_physics.force_normal = math.Vector(x, y).normal()
			# follow mouse
			elif const.CONTROL_MODE == const.CONTROL_MOUSE:
				if component_input.mouse_state['active'] and pygame.K_SPACE not in component_input.key_down:
					cur_pos = int(component_transform.position.x), int(component_transform.position.y)
					mouse_pos = pygame.mouse.get_pos()
					if mouse_pos[0] - cur_pos[0] != 0 or mouse_pos[1] - cur_pos[1] != 0:
						component_physics.force_normal = (math.Vector(*mouse_pos) - math.Vector(*cur_pos)).normal()
			# archery
			elif const.CONTROL_MODE == const.CONTROL_LINE:
				cur_pos = component_transform.position
				mouse_pos = pygame.mouse.get_pos()
				if 1 in component_input.mouse_state['trigger_down'] and not component_control.line_stage == 3:
					# line begin draw
					if (math.Vector(*mouse_pos) - cur_pos).length() < const.ENTITY_RADIUS:
						component_control.line_stage = 1
						component_control.line_start = cur_pos
						component_control.line_end = mouse_pos
					# line over
					else:
						line_reset(component_control)
				# line drawing
				if component_control.line_stage == 1:
					component_control.line_start = cur_pos
					component_control.line_end = mouse_pos
				# line draw over
				if component_control.line_stage == 1 and 1 in component_input.mouse_state['trigger_up']:
					component_control.line_stage = 2
				# line begin trigger
				if component_control.line_stage == 2 and 3 in component_input.mouse_state['trigger_up']:
					f_dir = math.Vector(*component_control.line_end) - component_control.line_start
					f_k = f_dir.length() / const.CONTROL_LINE_RADIUS
					component_control.line_f_dir = f_dir.normal()
					component_control.line_t = const.CONTROL_LINE_TIME * f_k if f_k < 1 else const.CONTROL_LINE_TIME
					component_control.line_stage = 3
				# line triggering
				if component_control.line_stage == 3:
					if component_control.line_t > 0:
						component_physics.force_normal = component_control.line_f_dir
						component_control.line_t = component_control.line_t - dt
					else:
						# line trigger over
						line_reset(component_control)
				# draw line
				if component_control.line_stage == 1 or component_control.line_stage == 2:
					# TODO draw to entity's render
					comp_render = component_control.entity.get_comp('comp_render')
					args_line = const.CONTROL_LINE_COLOR, component_control.line_start.tuple(), component_control.line_end
					comp_render.add_render(pygame.draw.aaline, args_line)
					if component_control.line_stage == 1:
						args_circle = const.CONTROL_LINE_COLOR, component_control.line_start.tuple(), const.CONTROL_LINE_RADIUS, const.CONTROL_LINE_WIDTH
						comp_render.add_render(pygame.draw.circle, args_circle)


def line_reset(component_control):
	component_control.line_stage = 0
	component_control.line_start = None
	component_control.line_end = None
	component_control.line_f_dir = None
	component_control.line_t = 0
