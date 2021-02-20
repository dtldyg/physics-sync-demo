# coding=utf-8

import time
import pygame
import base.const as const
import base.ecs as ecs


class ComponentInfo(ecs.Component):
	def __init__(self):
		super(ComponentInfo, self).__init__(ecs.LABEL_INFO)
		self.master_entity_id = 0
		self.font = pygame.font.SysFont('arial', 16)
		self.fps_frame = 0
		self.fps_lt = time.time()
		self.fps_txt = self.font.render('fps:0', True, const.FPS_COLOR)
