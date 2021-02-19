# coding=utf-8

import pygame
import pygame_gui
import common.base.const as const
import ecs.component as component


# TODO game 上
class ComponentGUI(component.Component):
	def __init__(self):
		super(ComponentGUI, self).__init__(component.LABEL_GUI)
		self.ui_manager = pygame_gui.UIManager((const.SCREEN_SIZE[0] + const.GUI_WIDTH, const.SCREEN_SIZE[1]))
		self.ui_bg = pygame.Surface((const.GUI_WIDTH, const.SCREEN_SIZE[1]), pygame.SRCALPHA)

		self.control_mod = None
		self.master_predict = None
		self.master_predict_server = None
		self.replica_buffer = None
		self.replica_interpolation = None
		self.replica_extrapolation = None

		# init
		self.ui_manager.get_root_container().set_position((const.SCREEN_SIZE[0], 0))
		self.ui_bg.fill(const.GUI_BACKGROUND)

		# ui elements
		ui_num = 0
		ui_num, y = next_ui_y(ui_num)
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

		ui_num, y = next_ui_y(ui_num)
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

		ui_num, y = next_ui_y(ui_num)
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='M_Server',
			manager=self.ui_manager
		)
		self.master_predict_server = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text=const.MASTER_SERVER.__str__(),
			manager=self.ui_manager)
		if const.MASTER_SERVER:
			self.master_predict_server.select()

		ui_num, y = next_ui_y(ui_num)
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

		ui_num, y = next_ui_y(ui_num)
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

		ui_num, y = next_ui_y(ui_num)
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


def next_ui_y(ui_num):
	return ui_num + 1, const.GUI_MARGIN[1] + (const.GUI_MARGIN[2] + const.GUI_SIZE[2]) * ui_num
