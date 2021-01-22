# coding=utf-8

import queue
import common.const as const
import common.math as math
import client.io as io


class CompState(object):
	def __init__(self, entity):
		self.entity = entity
		if entity.is_master:
			self.pos = math.Vector(*const.MASTER_INIT_POS)

	def update(self, _):
		if self.entity.is_shadow:
			# input sync
			while True:
				try:
					pkg = io.recv_q.get_nowait()
				except queue.Empty:
					break
				if pkg['cmd'] == 'sync':
					self.pos = math.Vector(**pkg['p'])
		else:
			# output sync
			# TODO 改为网络帧
			pkg = {'p': {'x': self.pos.x, 'y': self.pos.y}, 'v': {'x': 0, 'y': 0}}
			io.send_q.put(pkg)
