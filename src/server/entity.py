# coding=utf-8

import server.comp_state as comp_state
import server.comp_physics as comp_physics


class ServerEntity(object):
	def __init__(self, client_id):
		self.id = client_id
		self.comp_physics = comp_physics.CompPhysics(self)
		self.comp_state = comp_state.CompState(self)

	def update(self, dt):
		self.comp_physics.update(dt)
		self.comp_state.update(dt)
