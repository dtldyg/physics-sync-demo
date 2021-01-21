# coding=utf-8

import time
import common.math as math
import common.const as const
import client.comp_control as comp_control
import client.comp_physics as comp_physics
import client.comp_render as comp_render


class MasterEntity(object):
	def __init__(self):
		self.lt = time.time()
		self.color = const.MASTER_COLOR
		self.radius = const.ENTITY_RADIUS
		self.pos = math.Vector(*const.MASTER_INIT_POS)
		self.comp_control = comp_control.CompControl(self)
		self.comp_physics = comp_physics.CompPhysics(self)
		self.comp_render = comp_render.CompRender(self)

	def update(self, dt):
		self.comp_control.update(dt)
		self.comp_physics.update(dt)
		self.comp_render.update(dt)
