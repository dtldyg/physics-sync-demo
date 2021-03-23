# coding=utf-8

import pygame
import base.const as const
import base.ecs as ecs


class ComponentSurface(ecs.Component):
	def __init__(self):
		super(ComponentSurface, self).__init__(ecs.LABEL_SURFACE)
		self.game = pygame.Surface(const.SCREEN_SIZE, pygame.SRCALPHA)
		window_width = const.SCREEN_SIZE[0]
		if const.IS_CLIENT:
			window_width += const.GUI_WIDTH
			self.gui = pygame.Surface((const.SCREEN_SIZE[0] + const.GUI_WIDTH, const.SCREEN_SIZE[1]), pygame.SRCALPHA)
		self.window = pygame.display.set_mode((window_width, const.SCREEN_SIZE[1]))
