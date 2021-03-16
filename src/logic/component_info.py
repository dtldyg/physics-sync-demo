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
		self.fps_lt = time.time()
		self.render_fps = 0
		self.logic_fps = 0
		self.render_fps_txt = self.font.render('render_fps:0', True, const.FPS_COLOR)
		self.logic_fps_txt = self.font.render('logic_fps:0', True, const.FPS_COLOR)
