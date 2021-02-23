# coding=utf-8

import base.const as const
import base.ecs as ecs


class ComponentFrame(ecs.Component):
	def __init__(self):
		super(ComponentFrame, self).__init__(ecs.LABEL_FRAME)
		self.frame = 0
		if const.IS_CLIENT:
			self.server_frame = 0
