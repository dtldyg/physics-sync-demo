# coding=utf-8

import pygame
import pygame_gui
import base.const as const
import base.ecs as ecs


class ComponentGUI(ecs.Component):
	def __init__(self):
		super(ComponentGUI, self).__init__(ecs.LABEL_GUI)
		self.ui_manager = pygame_gui.UIManager((const.SCREEN_SIZE[0] + const.GUI_WIDTH, const.SCREEN_SIZE[1]), 'res/theme.json')
		self.ui_bg = pygame.Surface((const.GUI_WIDTH, const.SCREEN_SIZE[1]), pygame.SRCALPHA)

		self.control_mod = None
		self.show_server = None
		self.master_predict = None
		self.input_buffer = None
		self.replica_interpolation = None
		self.replica_extrapolation = None

		# init
		self.ui_manager.get_root_container().set_position((const.SCREEN_SIZE[0], 0))
		self.ui_bg.fill(const.GUI_BACKGROUND)

		# ui elements
		ui_num = 0
		container = pygame_gui.elements.UIScrollingContainer(
			relative_rect=pygame.Rect((0, 0), (const.GUI_WIDTH, const.SCREEN_SIZE[1])),
			manager=self.ui_manager
		)

		ui_num, y = next_ui_y(ui_num)
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_MARGIN[3] + const.GUI_SIZE[0] + const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text='全局设置',
			manager=self.ui_manager,
			container=container,
		)

		ui_num, y = next_ui_y(ui_num)
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='控制方式',
			manager=self.ui_manager,
			container=container,
		)
		self.control_mod = pygame_gui.elements.UIDropDownMenu(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			options_list=const.CONTROL_MODE_LIST,
			starting_option=const.CONTROL_MODE,
			manager=self.ui_manager,
			container=container,
		)

		ui_num, y = next_ui_y(ui_num)
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='显示服务端',
			manager=self.ui_manager,
			container=container,
		)
		self.show_server = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text=const.SHOW_SERVER.__str__(),
			manager=self.ui_manager,
			container=container,
		)
		if const.SHOW_SERVER:
			self.show_server.select()

		ui_num, y = next_ui_y(ui_num)
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='输入缓冲',
			manager=self.ui_manager,
			container=container,
		)
		self.input_buffer = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text=const.INPUT_BUFFER.__str__(),
			manager=self.ui_manager,
			container=container,
		)
		if const.INPUT_BUFFER:
			self.input_buffer.select()

		ui_num, y = next_ui_y(ui_num)
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_MARGIN[3] + const.GUI_SIZE[0] + const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text='主控设置',
			manager=self.ui_manager,
			container=container,
		)

		ui_num, y = next_ui_y(ui_num)
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='预测',
			manager=self.ui_manager,
			container=container,
		)
		self.master_predict = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text=const.MASTER_PREDICT.__str__(),
			manager=self.ui_manager,
			container=container,
		)
		if const.MASTER_PREDICT:
			self.master_predict.select()

		ui_num, y = next_ui_y(ui_num)
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='内插值',
			manager=self.ui_manager,
			container=container,
		)
		self.master_interpolation = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text=const.MASTER_INTERPOLATION.__str__(),
			manager=self.ui_manager,
			container=container,
		)
		if const.MASTER_INTERPOLATION:
			self.master_interpolation.select()

		ui_num, y = next_ui_y(ui_num)
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_MARGIN[3] + const.GUI_SIZE[0] + const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text='副本设置',
			manager=self.ui_manager,
			container=container,
		)

		ui_num, y = next_ui_y(ui_num)
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='内插值',
			manager=self.ui_manager,
			container=container,
		)
		self.replica_interpolation = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text=const.REPLICA_INTERPOLATION.__str__(),
			manager=self.ui_manager,
			container=container,
		)
		if const.REPLICA_INTERPOLATION:
			self.replica_interpolation.select()

		ui_num, y = next_ui_y(ui_num)
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='- 算法',
			manager=self.ui_manager,
			container=container,
		)
		self.replica_interpolation_mod = pygame_gui.elements.UIDropDownMenu(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			options_list=const.REPLICA_INTERPOLATION_LIST,
			starting_option=const.REPLICA_INTERPOLATION_MODE,
			manager=self.ui_manager,
			container=container,
		)

		ui_num, y = next_ui_y(ui_num)
		pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect((const.GUI_MARGIN[0], y), (const.GUI_SIZE[0], const.GUI_SIZE[2])),
			text='外插值',
			manager=self.ui_manager,
			container=container,
		)
		self.replica_extrapolation = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(
				(const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0], y), (const.GUI_SIZE[1], const.GUI_SIZE[2])),
			text=const.REPLICA_EXTRAPOLATION.__str__(),
			manager=self.ui_manager,
			container=container,
		)
		if const.REPLICA_EXTRAPOLATION:
			self.replica_extrapolation.select()

		_, y = next_ui_y(ui_num)
		container.set_scrollable_area_dimensions((const.GUI_MARGIN[0] + const.GUI_MARGIN[3] + const.GUI_SIZE[0] + const.GUI_SIZE[1], y + const.GUI_MARGIN[1]))


def next_ui_y(ui_num):
	return ui_num + 1, const.GUI_MARGIN[1] + (const.GUI_MARGIN[2] + const.GUI_SIZE[2]) * ui_num
