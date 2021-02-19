# coding=utf-8

import time
import pygame
import common.base.const as const
import ecs.component as component


# TODO game 上
class ComponentInfo(component.Component):
	def __init__(self):
		super(ComponentInfo, self).__init__(component.LABEL_INFO)
		self.info_font = pygame.font.SysFont('arial', 16)
		self.fps_frame = 0
		self.fps_lt = time.time()
		self.fps_txt = self.info_font.render('fps:0', True, const.FPS_COLOR)
