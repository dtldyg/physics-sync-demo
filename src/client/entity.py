# coding=utf-8

import common.base.const as const
import common.ec as ec

import client.comp_control as comp_control
import client.comp_physics as comp_physics
import client.comp_state as comp_state
import client.comp_render as comp_render


class MasterEntity(ClientEntity):
	def __init__(self):
		super(MasterEntity, self).__init__(flags=(const.ENTITY_FLAG_MASTER, const.ENTITY_FLAG_LOCAL))
		self.add_comp(comp_control.CompControl())
		self.add_comp(comp_physics.CompPhysics())
		self.add_comp(comp_state.CompState())
		self.add_comp(comp_render.CompRender())

	def output_cmd(self):
		cmd = {'eid': self.eid}
		self.iter_comps(lambda c: c.output_cmd(cmd))
		return cmd


class ClientComponent(ec.Component):
	def input_state(self, pkg):
		pass


class MasterComponent(ClientComponent):
	def output_cmd(self, cmd):
		pass
