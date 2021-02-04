# coding=utf-8

import common.base.ec as ec

import server.comp_control as comp_control
import server.comp_physics as comp_physics
import server.comp_state as comp_state


class ServerEntity(ec.Entity):
	def __init__(self, send_q):
		super(ServerEntity, self).__init__()
		self.send_q = send_q
		self.add_comp(comp_control.CompControl())
		self.add_comp(comp_physics.CompPhysics())
		self.add_comp(comp_state.CompState())

	def input_cmd(self, pkg):
		self.iter_comps(lambda c: c.input_cmd(pkg))

	def output_state(self):
		state = {'eid': self.eid}
		self.iter_comps(lambda c: c.output_state(state))
		return state


class ServerComponent(ec.Component):
	def input_cmd(self, pkg):
		pass

	def output_state(self, state):
		pass
