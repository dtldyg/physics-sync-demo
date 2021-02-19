# coding=utf-8

import pygame
import common.base.const as const
import common.base.math as math
import ecs.component as component


class ComponentRender(component.Component):
	def __init__(self):
		super(ComponentRender, self).__init__(component.LABEL_RENDER)
		self.client_surface = None
		self.client_interpolation = [None, 0, None, 0]
		self.server_surface = None
		self.server_interpolation = [None, 0, None, 0]
		self.other_renders = []

		# init
		c_sur = pygame.Surface((const.ENTITY_RADIUS * 2, const.ENTITY_RADIUS * 2), pygame.SRCALPHA)
		pygame.draw.circle(c_sur, const.MASTER_CLIENT_COLOR, (const.ENTITY_RADIUS, const.ENTITY_RADIUS), const.ENTITY_RADIUS)
		self.client_surface = (c_sur, math.Vector(const.ENTITY_RADIUS, const.ENTITY_RADIUS))
		s_sur = pygame.Surface((const.ENTITY_RADIUS * 2, const.ENTITY_RADIUS * 2), pygame.SRCALPHA)
		pygame.draw.circle(s_sur, const.MASTER_SERVER_COLOR, (const.ENTITY_RADIUS, const.ENTITY_RADIUS), const.ENTITY_RADIUS)
		self.server_surface = (s_sur, math.Vector(const.ENTITY_RADIUS, const.ENTITY_RADIUS))
