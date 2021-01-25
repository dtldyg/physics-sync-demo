# coding=utf-8

import common.math as math
import common.ec as ec


class CompState(ec.Component):
	def __init__(self):
		super(CompState, self).__init__('comp_state')
		self.dirty = False
		self.velocity = math.Vector()
		self.pos = math.Vector()

	def io_in(self, pkg):
		if pkg['cmd'] == 'sync':
			self.dirty = True
			self.velocity = math.Vector(**pkg['v'])
			self.pos = math.Vector(**pkg['p'])

	def io_out(self):
		if self.dirty:
			self.dirty = False
			pkg = {'cmd': 'sync', 'v': {'x': self.velocity.x, 'y': self.velocity.y}, 'p': {'x': self.pos.x, 'y': self.pos.y}}
			self.entity.send_q.put(pkg)
