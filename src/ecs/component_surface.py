# coding=utf-8

import pygame
import common.base.const as const
import ecs.component as component


# TODO game 上
class ComponentSurface(component.Component):
	def __init__(self):
		super(ComponentSurface, self).__init__(component.LABEL_SURFACE)
		self.window = pygame.display.set_mode((const.SCREEN_SIZE[0] + const.GUI_WIDTH, const.SCREEN_SIZE[1]))
		self.game = pygame.Surface(const.SCREEN_SIZE, pygame.SRCALPHA)
		self.gui = pygame.Surface((const.SCREEN_SIZE[0] + const.GUI_WIDTH, const.SCREEN_SIZE[1]), pygame.SRCALPHA)
