# coding=utf-8

import common.const as const
import common.math as math

import client.io as io


class CompState(object):
	def __init__(self, entity):
		self.entity = entity
		if entity.is_master:
			self.pos = math.Vector(*const.MASTER_INIT_POS)
		else:
			self.pos = math.Vector(*const.REPLICA_INIT_POS)

	def update(self, _):
		pass

	def sync_out(self):
		if self.entity.is_master and not self.entity.is_shadow:
			pkg = {'p': {'x': self.pos.x, 'y': self.pos.y}, 'v': {'x': 0, 'y': 0}}
			io.send_q.put(pkg)

	def sync_in(self, pkg):
		if self.entity.is_master and self.entity.is_shadow:
			if pkg['cmd'] == 'sync':
				self.pos = math.Vector(**pkg['p'])
