# coding=utf-8

import common.ec as ec

import server.comp_control as comp_control
import server.comp_physics as comp_physics
import server.comp_state as comp_state


class ServerEntity(ec.ServerEntity):
	def __init__(self, send_q):
		super(ServerEntity, self).__init__()
		self.send_q = send_q
		self.add_comp(comp_control.CompControl())
		self.add_comp(comp_physics.CompPhysics())
		self.add_comp(comp_state.CompState())
