# coding=utf-8

import base.ecs as ecs


class ComponentFrame(ecs.Component):
	def __init__(self):
		super(ComponentFrame, self).__init__(ecs.LABEL_FRAME)
		self.frame = 0
