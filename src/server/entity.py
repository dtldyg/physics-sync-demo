# coding=utf-8

import common.ec as ec

import server.comp_state as comp_state
import server.comp_physics as comp_physics


class ServerEntity(ec.Entity):
	def __init__(self, client_id, send_q):
		super(ServerEntity, self).__init__()
		self.client_id = client_id
		self.send_q = send_q
		self.add_comp(comp_physics.CompPhysics())
		self.add_comp(comp_state.CompState())
