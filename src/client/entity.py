# coding=utf-8

import common.base.const as const
import common.base.ec as ec

import client.comp_control as comp_control
import client.comp_physics as comp_physics
import client.comp_state as comp_state
import client.comp_render as comp_render


class ClientEntity(ec.Entity):
	def __init__(self, flags=()):
		super(ClientEntity, self).__init__()
		self.flags = 0
		for flag in flags:
			if flag[1] == 1:
				self.flags = self.flags | flag[0]

	def has_flags(self, *flags):
		for flag in flags:
			if self.flags & flag[0] != flag[0] * flag[1]:
				return False
		return True


class MasterEntity(ClientEntity):
	def __init__(self):
		super(MasterEntity, self).__init__(flags=(const.ENTITY_FLAG_MASTER, const.ENTITY_FLAG_LOCAL))
		self.add_comp(comp_control.CompControl())
		self.add_comp(comp_physics.CompPhysics())
		self.add_comp(comp_state.CompState())
		self.add_comp(comp_render.CompRender())


class MasterShadowEntity(ClientEntity):
	def __init__(self):
		super(MasterShadowEntity, self).__init__(flags=(const.ENTITY_FLAG_MASTER, const.ENTITY_FLAG_SHADOW))
		self.add_comp(comp_state.CompState())
		self.add_comp(comp_render.CompRender())
