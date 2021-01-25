# coding=utf-8

import common.const as const
import common.ec as ec

import client.comp_control as comp_control
import client.comp_physics as comp_physics
import client.comp_state as comp_state
import client.comp_render as comp_render


class MasterEntity(ec.Entity):
	def __init__(self):
		super(MasterEntity, self).__init__((const.ENTITY_FLAG_MASTER, const.ENTITY_FLAG_LOCAL))
		self.add_comp(comp_control.CompControl())
		self.add_comp(comp_physics.CompPhysics())
		self.add_comp(comp_state.CompState())
		self.add_comp(comp_render.CompRender())


class MasterShadowEntity(ec.Entity):
	def __init__(self):
		super(MasterShadowEntity, self).__init__((const.ENTITY_FLAG_MASTER, const.ENTITY_FLAG_SHADOW))
		self.add_comp(comp_state.CompState())
		self.add_comp(comp_render.CompRender())
