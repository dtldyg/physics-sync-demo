# coding=utf-8

import pygame
import base.const as const
import base.math as math
import base.ecs as ecs


class ComponentRender(ecs.Component):
	def __init__(self, is_master=False):
		super(ComponentRender, self).__init__(ecs.LABEL_RENDER)
		self.client_surface = None
		self.server_surface = None
		self.interpolation = [None, 0, None, 0]
		self.other_renders = []

		# init
		c_color = const.MASTER_CLIENT_COLOR if is_master else const.REPLICA_CLIENT_COLOR
		s_color = const.MASTER_SERVER_COLOR if is_master else const.REPLICA_SERVER_COLOR
		c_sur = pygame.Surface((const.ENTITY_RADIUS * 2, const.ENTITY_RADIUS * 2), pygame.SRCALPHA)
		# c_sur.fill(c_color)  # test square
		pygame.draw.circle(c_sur, c_color, (const.ENTITY_RADIUS, const.ENTITY_RADIUS), const.ENTITY_RADIUS)
		self.client_surface = (c_sur, math.Vector(const.ENTITY_RADIUS, const.ENTITY_RADIUS))
		s_sur = pygame.Surface((const.ENTITY_RADIUS * 2, const.ENTITY_RADIUS * 2), pygame.SRCALPHA)
		# s_sur.fill(s_color)  # test square
		pygame.draw.circle(s_sur, s_color, (const.ENTITY_RADIUS, const.ENTITY_RADIUS), const.ENTITY_RADIUS)
		self.server_surface = (s_sur, math.Vector(const.ENTITY_RADIUS, const.ENTITY_RADIUS))
