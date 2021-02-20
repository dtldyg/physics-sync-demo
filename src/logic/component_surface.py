# coding=utf-8

import pygame
import base.const as const
import base.ecs as ecs


class ComponentSurface(ecs.Component):
	def __init__(self):
		super(ComponentSurface, self).__init__(ecs.LABEL_SURFACE)
		self.window = pygame.display.set_mode((const.SCREEN_SIZE[0] + const.GUI_WIDTH, const.SCREEN_SIZE[1]))
		self.game = pygame.Surface(const.SCREEN_SIZE, pygame.SRCALPHA)
		self.gui = pygame.Surface((const.SCREEN_SIZE[0] + const.GUI_WIDTH, const.SCREEN_SIZE[1]), pygame.SRCALPHA)
