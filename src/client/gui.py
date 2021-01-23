# coding=utf-8

import pygame
import pygame_gui
import client.window as window
import common.const as const
import common.switch as switch


class GUI(object):
	def __init__(self):
		self.ui_manager = pygame_gui.UIManager((const.SCREEN_SIZE[0] + const.PANEL_WIDTH, const.SCREEN_SIZE[1]))
		self.ui_manager.get_root_container().set_position((const.SCREEN_SIZE[0], 0))

		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((8, 14), (100, 20)),
			text='ControlMod',
			manager=self.ui_manager
		)
		self.control_mod = pygame_gui.elements.UIDropDownMenu(
			options_list=['WASD', 'Mouse Follow', 'Mouse Line'],
			starting_option='WASD',
			relative_rect=pygame.Rect((108, 10), (140, 26)),
			manager=self.ui_manager
		)

	def update(self, dt):
		self.ui_manager.update(dt)
		self.ui_manager.draw_ui(window.panel)

	def process_events(self, event):
		self.ui_manager.process_events(event)
		if event.type == pygame.USEREVENT:
			if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
				if event.ui_element == self.control_mod:
					if event.text == 'WASD':
						switch.CONTROL_MODE = switch.CONTROL_WASD
					elif event.text == 'Mouse Follow':
						switch.CONTROL_MODE = switch.CONTROL_MOUSE
					elif event.text == 'Mouse Line':
						switch.CONTROL_MODE = switch.CONTROL_LINE
