# coding=utf-8

import pygame
import pygame_gui

import common.const as const
import common.switch as switch

import client.window as window


class GUI(object):
	def __init__(self):
		self.ui_num = 0
		self.ui_manager = pygame_gui.UIManager((const.SCREEN_SIZE[0] + const.PANEL_WIDTH, const.SCREEN_SIZE[1]))
		self.ui_manager.get_root_container().set_position((const.SCREEN_SIZE[0], 0))

		y = self.next_ui_y()
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.PANEL_UI_MARGIN[0], y), (const.PANEL_UI_SIZE[0], const.PANEL_UI_SIZE[2])),
			text='Control',
			manager=self.ui_manager
		)
		self.control_mod = pygame_gui.elements.UIDropDownMenu(
			relative_rect=pygame.Rect(
				(const.PANEL_UI_MARGIN[0] + const.PANEL_UI_MARGIN[3] + const.PANEL_UI_SIZE[0], y), (const.PANEL_UI_SIZE[1], const.PANEL_UI_SIZE[2])),
			options_list=switch.CONTROL_MODE_LIST,
			starting_option=switch.CONTROL_MODE,
			manager=self.ui_manager
		)

		y = self.next_ui_y()
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.PANEL_UI_MARGIN[0], y), (const.PANEL_UI_SIZE[0], const.PANEL_UI_SIZE[2])),
			text='M_Predict',
			manager=self.ui_manager
		)
		self.master_predict = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.PANEL_UI_MARGIN[0] + const.PANEL_UI_MARGIN[3] + const.PANEL_UI_SIZE[0], y), (const.PANEL_UI_SIZE[1], const.PANEL_UI_SIZE[2])),
			text=switch.MASTER_PREDICT.__str__(),
			manager=self.ui_manager)
		if switch.MASTER_PREDICT:
			self.master_predict.select()

		y = self.next_ui_y()
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.PANEL_UI_MARGIN[0], y), (const.PANEL_UI_SIZE[0], const.PANEL_UI_SIZE[2])),
			text='M_Buffer',
			manager=self.ui_manager
		)
		self.master_buffer = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.PANEL_UI_MARGIN[0] + const.PANEL_UI_MARGIN[3] + const.PANEL_UI_SIZE[0], y), (const.PANEL_UI_SIZE[1], const.PANEL_UI_SIZE[2])),
			text=switch.MASTER_BUFFER.__str__(),
			manager=self.ui_manager)
		if switch.MASTER_BUFFER:
			self.master_buffer.select()

		y = self.next_ui_y()
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.PANEL_UI_MARGIN[0], y), (const.PANEL_UI_SIZE[0], const.PANEL_UI_SIZE[2])),
			text='M_InterP',
			manager=self.ui_manager
		)
		self.master_interpolation = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.PANEL_UI_MARGIN[0] + const.PANEL_UI_MARGIN[3] + const.PANEL_UI_SIZE[0], y), (const.PANEL_UI_SIZE[1], const.PANEL_UI_SIZE[2])),
			text=switch.MASTER_INTERPOLATION.__str__(),
			manager=self.ui_manager)
		if switch.MASTER_INTERPOLATION:
			self.master_interpolation.select()

		y = self.next_ui_y()
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.PANEL_UI_MARGIN[0], y), (const.PANEL_UI_SIZE[0], const.PANEL_UI_SIZE[2])),
			text='M_ExtraP',
			manager=self.ui_manager
		)
		self.master_extrapolation = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.PANEL_UI_MARGIN[0] + const.PANEL_UI_MARGIN[3] + const.PANEL_UI_SIZE[0], y), (const.PANEL_UI_SIZE[1], const.PANEL_UI_SIZE[2])),
			text=switch.MASTER_EXTRAPOLATION.__str__(),
			manager=self.ui_manager)
		if switch.MASTER_EXTRAPOLATION:
			self.master_extrapolation.select()

	def update(self, dt):
		self.ui_manager.update(dt)
		self.ui_manager.draw_ui(window.panel)

	def next_ui_y(self):
		self.ui_num = self.ui_num + 1
		return const.PANEL_UI_MARGIN[1] + (const.PANEL_UI_MARGIN[2] + const.PANEL_UI_SIZE[2]) * (self.ui_num - 1)

	def process_events(self, event):
		self.ui_manager.process_events(event)
		if event.type == pygame.USEREVENT:
			if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
				if event.ui_element == self.control_mod:
					switch.CONTROL_MODE = event.text
			if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
				if event.ui_element == self.master_predict:
					selected = False
					if event.ui_element.is_selected:
						event.ui_element.unselect()
					else:
						event.ui_element.select()
						selected = True
					event.ui_element.set_text(selected.__str__())
					switch.MASTER_PREDICT = selected
				elif event.ui_element == self.master_buffer:
					selected = False
					if event.ui_element.is_selected:
						event.ui_element.unselect()
					else:
						event.ui_element.select()
						selected = True
					event.ui_element.set_text(selected.__str__())
					switch.MASTER_BUFFER = selected
				elif event.ui_element == self.master_interpolation:
					selected = False
					if event.ui_element.is_selected:
						event.ui_element.unselect()
					else:
						event.ui_element.select()
						selected = True
					event.ui_element.set_text(selected.__str__())
					switch.MASTER_INTERPOLATION = selected
				elif event.ui_element == self.master_extrapolation:
					selected = False
					if event.ui_element.is_selected:
						event.ui_element.unselect()
					else:
						event.ui_element.select()
						selected = True
					event.ui_element.set_text(selected.__str__())
					switch.MASTER_EXTRAPOLATION = selected
