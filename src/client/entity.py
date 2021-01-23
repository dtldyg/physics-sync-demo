# coding=utf-8

import client.comp_control as comp_control
import client.comp_physics as comp_physics
import client.comp_state as comp_state
import client.comp_render as comp_render


class MasterEntity(object):
	def __init__(self):
		self.is_master = True
		self.is_shadow = False
		self.comp_control = comp_control.CompControl(self)
		self.comp_physics = comp_physics.CompPhysics(self)
		self.comp_state = comp_state.CompState(self)
		self.comp_render = comp_render.CompRender(self)

	def update(self, dt):
		self.comp_control.update(dt)
		self.comp_physics.update(dt)
		self.comp_state.update(dt)
		self.comp_render.update(dt)

	def sync_out(self):
		self.comp_control.sync_out()
		self.comp_physics.sync_out()
		self.comp_state.sync_out()
		self.comp_render.sync_out()

	def sync_in(self, pkg):
		self.comp_control.sync_in(pkg)
		self.comp_physics.sync_in(pkg)
		self.comp_state.sync_in(pkg)
		self.comp_render.sync_in(pkg)


class MasterShadowEntity(object):
	def __init__(self):
		self.is_master = True
		self.is_shadow = True
		self.comp_state = comp_state.CompState(self)
		self.comp_render = comp_render.CompRender(self)

	def update(self, dt):
		self.comp_state.update(dt)
		self.comp_render.update(dt)

	def sync_out(self):
		self.comp_state.sync_out()
		self.comp_render.sync_out()

	def sync_in(self, pkg):
		self.comp_state.sync_in(pkg)
		self.comp_render.sync_in(pkg)
