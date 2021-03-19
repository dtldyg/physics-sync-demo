# coding=utf-8

import queue
import base.ecs as ecs
import base.const as const


class ComponentPackage(ecs.Component):
	def __init__(self):
		super(ComponentPackage, self).__init__(ecs.LABEL_PACKAGE)
		self.packages = []
		if const.IS_SERVER:
			self.buffer_state = 0
			self.buffer = queue.Queue(1024)
			self.last_buffer_size = 0
