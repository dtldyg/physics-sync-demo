# coding=utf-8

import ecs.component as component


class ComponentFrame(component.Component):
	def __init__(self):
		super(ComponentFrame, self).__init__(component.LABEL_FRAME)
		self.frame = 0
