# coding=utf-8

import pygame
import pygame_gui
import base.clock as clock
import base.const as const
import base.ecs as ecs


class SystemGameEvent(ecs.System):
	def __init__(self):
		super(SystemGameEvent, self).__init__((ecs.LABEL_INPUT, ecs.LABEL_GUI))

	def update(self, dt, component_tuples):
		for _, comp_tuple in component_tuples:
			comp_input, comp_gui = comp_tuple
			comp_input.mouse_state['trigger_down'].clear()
			comp_input.mouse_state['trigger_up'].clear()
			for event in pygame.event.get():
				# quit
				if event.type == pygame.QUIT:
					raise clock.QuitError()
				# key
				if event.type == pygame.KEYDOWN:
					comp_input.key_down.add(event.key)
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_ESCAPE:
						raise clock.QuitError()
					comp_input.key_down.remove(event.key)
				# mouse
				elif event.type == pygame.WINDOWENTER:
					comp_input.mouse_state['active'] = True
				elif event.type == pygame.WINDOWLEAVE:
					comp_input.mouse_state['active'] = False
				elif event.type == pygame.MOUSEBUTTONDOWN:
					comp_input.mouse_state['trigger_down'].add(event.button)
				elif event.type == pygame.MOUSEBUTTONUP:
					comp_input.mouse_state['trigger_up'].add(event.button)
				# gui
				elif event.type == pygame.USEREVENT:
					if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
						if event.ui_element == comp_gui.control_mod:
							const.CONTROL_MODE = event.text
						elif event.ui_element == comp_gui.replica_interpolation_mod:
							const.REPLICA_INTERPOLATION_MODE = event.text
					elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
						if event.ui_element == comp_gui.show_server:
							const.SHOW_SERVER = btn_checkbox_event(event)
						elif event.ui_element == comp_gui.input_buffer:
							const.INPUT_BUFFER = btn_checkbox_event(event)
						elif event.ui_element == comp_gui.master_predict:
							const.MASTER_PREDICT = btn_checkbox_event(event)
						elif event.ui_element == comp_gui.master_interpolation:
							const.MASTER_INTERPOLATION = btn_checkbox_event(event)
						elif event.ui_element == comp_gui.replica_interpolation:
							const.REPLICA_INTERPOLATION = btn_checkbox_event(event)
						elif event.ui_element == comp_gui.replica_extrapolation:
							const.REPLICA_EXTRAPOLATION = btn_checkbox_event(event)
				comp_gui.ui_manager.process_events(event)


def btn_checkbox_event(event):
	selected = False
	if event.ui_element.is_selected:
		event.ui_element.unselect()
	else:
		event.ui_element.select()
		selected = True
	event.ui_element.set_text(selected.__str__())
	return selected
