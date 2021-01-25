# coding=utf-8

import common.const as const
import common.math as math
import common.ec as ec

import client.io as io


class CompState(ec.Component):
	def __init__(self):
		super(CompState, self).__init__('comp_state')
		self.dirty = False
		self._velocity = math.Vector()
		self._pos = math.Vector()

	@property
	def velocity(self):
		return self._velocity

	@velocity.setter
	def velocity(self, value):
		if self._velocity != value:
			self.dirty = True
		self._velocity = value

	@property
	def pos(self):
		return self._pos

	@pos.setter
	def pos(self, value):
		if self._pos != value:
			self.dirty = True
		self._pos = value

	def init(self):
		if self.entity.has_flags(const.ENTITY_FLAG_MASTER):
			self.pos = math.Vector(*const.MASTER_INIT_POS)
		else:
			self.pos = math.Vector(*const.REPLICA_INIT_POS)

	def io_in(self, pkg):
		if self.entity.has_flags(const.ENTITY_FLAG_MASTER, const.ENTITY_FLAG_SHADOW):
			if pkg['cmd'] == 'sync':
				self.pos = math.Vector(**pkg['p'])

	def io_out(self):
		if self.entity.has_flags(const.ENTITY_FLAG_MASTER, const.ENTITY_FLAG_LOCAL) and self.dirty:
			pkg = {'p': {'x': self.pos.x, 'y': self.pos.y}, 'v': {'x': self.velocity.x, 'y': self.velocity.y}}
			io.send_q.put(pkg)
			self.dirty = False
