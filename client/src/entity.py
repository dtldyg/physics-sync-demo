# coding=utf-8

import time
import _math
import _const
import comp_control
import comp_physics
import comp_render


class MasterEntity(object):
	def __init__(self):
		self.lt = time.time()
		self.color = _const.MASTER_COLOR
		self.radius = _const.ENTITY_RADIUS
		self.pos = _math.Vector(*_const.MASTER_INIT_POS)
		self.comp_control = comp_control.CompControl(self)
		self.comp_physics = comp_physics.CompPhysics(self)
		self.comp_render = comp_render.CompRender(self)

	def update(self, dt):
		self.comp_control.update(dt)
		self.comp_physics.update(dt)
		self.comp_render.update(dt)
