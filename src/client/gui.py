# coding=utf-8

import pygame
import pygame_gui

import common.base.const as const


class GUI(object):
	def __init__(self, sur):
		self.sur = sur
		self.ui_num = 0
		self.ui_manager = pygame_gui.UIManager((const.SCREEN_SIZE[0] + const.GUI_WIDTH, const.SCREEN_SIZE[1]))
		self.ui_manager.get_root_container().set_position((const.SCREEN_SIZE[0], 0))
		self.bg = pygame.Surface((const.GUI_WIDTH, const.SCREEN_SIZE[1]), pygame.SRCALPHA)
		self.bg.fill(const.GUI_BACKGROUND)

		y = self.next_ui_y()
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='Control',
			manager=self.ui_manager
		)
		self.control_mod = pygame_gui.elements.UIDropDownMenu(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			options_list=const.CONTROL_MODE_LIST,
			starting_option=const.CONTROL_MODE,
			manager=self.ui_manager
		)

		y = self.next_ui_y()
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='M_Predict',
			manager=self.ui_manager
		)
		self.master_predict = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text=const.MASTER_PREDICT.__str__(),
			manager=self.ui_manager)
		if const.MASTER_PREDICT:
			self.master_predict.select()

		y = self.next_ui_y()
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='M_Pred_Svr',
			manager=self.ui_manager
		)
		self.master_predict_server = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text=const.MASTER_PREDICT_SERVER.__str__(),
			manager=self.ui_manager)
		if const.MASTER_PREDICT_SERVER:
			self.master_predict_server.select()

		y = self.next_ui_y()
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='R_Buffer',
			manager=self.ui_manager
		)
		self.replica_buffer = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text=const.REPLICA_BUFFER.__str__(),
			manager=self.ui_manager)
		if const.REPLICA_BUFFER:
			self.replica_buffer.select()

		y = self.next_ui_y()
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='R_InterP',
			manager=self.ui_manager
		)
		self.replica_interpolation = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text=const.REPLICA_INTERPOLATION.__str__(),
			manager=self.ui_manager)
		if const.REPLICA_INTERPOLATION:
			self.replica_interpolation.select()

		y = self.next_ui_y()
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='R_ExtraP',
			manager=self.ui_manager
		)
		self.replica_extrapolation = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text=const.REPLICA_EXTRAPOLATION.__str__(),
			manager=self.ui_manager)
		if const.REPLICA_EXTRAPOLATION:
			self.replica_extrapolation.select()

	def update(self, dt):
		self.sur.blit(self.bg, (const.SCREEN_SIZE[0], 0))
		self.ui_manager.update(dt)
		self.ui_manager.draw_ui(self.sur)

	def next_ui_y(self):
		self.ui_num = self.ui_num + 1
		return const.GUI_MARGIN[1] + (const.GUI_MARGIN[2] + const.GUI_SIZE[2]) * (self.ui_num - 1)

	def process_events(self, event):
		self.ui_manager.process_events(event)
		if event.type == pygame.USEREVENT:
			if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
				if event.ui_element == self.control_mod:
					const.CONTROL_MODE = event.text
			if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
				if event.ui_element == self.master_predict:
					const.MASTER_PREDICT = btn_checkbox_event(event)
				if event.ui_element == self.master_predict_server:
					const.MASTER_PREDICT_SERVER = btn_checkbox_event(event)
				elif event.ui_element == self.replica_buffer:
					const.REPLICA_BUFFER = btn_checkbox_event(event)
				elif event.ui_element == self.replica_interpolation:
					const.REPLICA_INTERPOLATION = btn_checkbox_event(event)
				elif event.ui_element == self.replica_extrapolation:
					const.REPLICA_EXTRAPOLATION = btn_checkbox_event(event)


def btn_checkbox_event(event):
	selected = False
	if event.ui_element.is_selected:
		event.ui_element.unselect()
	else:
		event.ui_element.select()
		selected = True
	event.ui_element.set_text(selected.__str__())
	return selected
