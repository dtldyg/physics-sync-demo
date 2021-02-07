# coding=utf-8

import common.base.const as const
import common.ec as ec

import client.comp_control as comp_control
import client.comp_physics as comp_physics
import client.comp_state as comp_state
import client.comp_render as comp_render


class MasterEntity(ec.ClientEntity):
	def __init__(self):
		super(MasterEntity, self).__init__()
		self.enable = False
		self.add_comp(comp_render.CompRender())
		self.add_comp(comp_control.CompControl())
		self.add_comp(comp_physics.CompPhysics())
		self.add_comp(comp_state.CompState())


class ReplicaEntity(ec.ClientEntity):
	def __init__(self):
		super(ReplicaEntity, self).__init__()
		self.add_comp(comp_render.CompRender())
		self.add_comp(comp_state.CompState())
