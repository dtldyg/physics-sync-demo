# coding=utf-8

import pygame
import base.const as const
import base.math as math
import base.ecs as ecs


class SystemControl(ecs.System):
	def __init__(self, world):
		super(SystemControl, self).__init__(world, (ecs.LABEL_CONTROL, ecs.LABEL_PHYSICS, ecs.LABEL_TRANSFORM, ecs.LABEL_RENDER))

	def update(self, dt, component_tuples):
		game_comp_input = self.world.game_component(ecs.LABEL_INPUT)
		for _, comp_tuple in component_tuples:
			comp_control, comp_physics, comp_transform, comp_render = comp_tuple
			comp_physics.force_normal = math.vector_zero

			# wasd
			if const.CONTROL_MODE == const.CONTROL_WASD:
				x, y = 0, 0
				if pygame.K_w in game_comp_input.key_down:
					y = -1
				if pygame.K_s in game_comp_input.key_down:
					y = 1
				if pygame.K_a in game_comp_input.key_down:
					x = -1
				if pygame.K_d in game_comp_input.key_down:
					x = 1
				if x != 0 or y != 0:
					comp_physics.force_normal = math.Vector(x, y).normal()
			# follow mouse
			elif const.CONTROL_MODE == const.CONTROL_MOUSE:
				if game_comp_input.mouse_state['active'] and pygame.K_SPACE in game_comp_input.key_down:
					if const.MASTER_BEHAVIOR != const.MASTER_SERVER:
						cur_pos = int(comp_transform.position.x), int(comp_transform.position.y)
					else:
						cur_pos = int(comp_transform.server_position.x), int(comp_transform.server_position.y)
					mouse_pos = pygame.mouse.get_pos()
					if mouse_pos[0] - cur_pos[0] != 0 or mouse_pos[1] - cur_pos[1] != 0:
						comp_physics.force_normal = (math.Vector(*mouse_pos) - math.Vector(*cur_pos)).normal()
			# archery
			elif const.CONTROL_MODE == const.CONTROL_LINE:
				cur_pos = comp_transform.position
				mouse_pos = pygame.mouse.get_pos()
				if 1 in game_comp_input.mouse_state['trigger_down'] and not comp_control.line_stage == 3:
					# line begin draw
					if (math.Vector(*mouse_pos) - cur_pos).length() < const.ENTITY_RADIUS:
						comp_control.line_stage = 1
						comp_control.line_start = cur_pos
						comp_control.line_end = mouse_pos
				# line cancel
				if 3 in game_comp_input.mouse_state['trigger_down']:
					line_reset(comp_control)
				# line drawing
				if comp_control.line_stage == 1:
					comp_control.line_start = cur_pos
					comp_control.line_end = mouse_pos
				# line draw over
				if comp_control.line_stage == 1 and 1 in game_comp_input.mouse_state['trigger_up']:
					comp_control.line_stage = 2
				# line begin trigger
				if comp_control.line_stage == 2 and 1 in game_comp_input.mouse_state['trigger_down']:
					f_dir = math.Vector(*comp_control.line_end) - comp_control.line_start
					f_k = f_dir.length() / const.CONTROL_LINE_RADIUS
					comp_control.line_f_dir = f_dir.normal()
					comp_control.line_t = const.CONTROL_LINE_TIME * f_k if f_k < 1 else const.CONTROL_LINE_TIME
					comp_control.line_stage = 3
				# line triggering
				if comp_control.line_stage == 3:
					if comp_control.line_t > 0:
						comp_physics.force_normal = comp_control.line_f_dir
						comp_control.line_t = comp_control.line_t - dt
					else:
						# line trigger over
						line_reset(comp_control)
				# draw line
				if comp_control.line_stage == 1 or comp_control.line_stage == 2:
					args_line = const.CONTROL_LINE_COLOR, comp_control.line_start.tuple(), comp_control.line_end
					comp_render.other_renders.append((pygame.draw.aaline, args_line))
					if comp_control.line_stage == 1:
						args_circle = const.CONTROL_LINE_COLOR, comp_control.line_start.tuple(), const.CONTROL_LINE_RADIUS, const.CONTROL_LINE_WIDTH
						comp_render.other_renders.append((pygame.draw.circle, args_circle))


def line_reset(component_control):
	component_control.line_stage = 0
	component_control.line_start = None
	component_control.line_end = None
	component_control.line_f_dir = None
	component_control.line_t = 0
