# coding=utf-8

import pygame
import pygame_gui
import common.base.clock as clock
import common.base.const as const
import ecs.system as system
import ecs.component as component


class SystemGameEvent(system.System):
	def __init__(self):
		super(SystemGameEvent, self).__init__((component.LABEL_INPUT, component.LABEL_GUI))

	def update(self, dt, component_tuples):
		for _, component_tuple in component_tuples:
			component_input, component_gui = component_tuple
			component_input.mouse_state['trigger_down'].clear()
			component_input.mouse_state['trigger_up'].clear()
			for event in pygame.event.get():
				# quit
				if event.type == pygame.QUIT:
					raise clock.QuitError()
				# key
				if event.type == pygame.KEYDOWN:
					component_input.key_down.add(event.key)
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_ESCAPE:
						raise clock.QuitError()
					component_input.key_down.remove(event.key)
				# mouse
				elif event.type == pygame.WINDOWENTER:
					component_input.mouse_state['active'] = True
				elif event.type == pygame.WINDOWLEAVE:
					component_input.mouse_state['active'] = False
				elif event.type == pygame.MOUSEBUTTONDOWN:
					component_input.mouse_state['trigger_down'].add(event.button)
				elif event.type == pygame.MOUSEBUTTONUP:
					component_input.mouse_state['trigger_up'].add(event.button)
				# gui
				elif event.type == pygame.USEREVENT:
					if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
						if event.ui_element == component_gui.control_mod:
							const.CONTROL_MODE = event.text
					elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
						if event.ui_element == component_gui.master_predict:
							const.MASTER_PREDICT = btn_checkbox_event(event)
						if event.ui_element == component_gui.master_predict_server:
							const.MASTER_SERVER = btn_checkbox_event(event)
						elif event.ui_element == component_gui.replica_buffer:
							const.REPLICA_BUFFER = btn_checkbox_event(event)
						elif event.ui_element == component_gui.replica_interpolation:
							const.REPLICA_INTERPOLATION = btn_checkbox_event(event)
						elif event.ui_element == component_gui.replica_extrapolation:
							const.REPLICA_EXTRAPOLATION = btn_checkbox_event(event)
				component_gui.ui_manager.process_events(event)


def btn_checkbox_event(event):
	selected = False
	if event.ui_element.is_selected:
		event.ui_element.unselect()
	else:
		event.ui_element.select()
		selected = True
	event.ui_element.set_text(selected.__str__())
	return selected
