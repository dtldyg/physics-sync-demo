# coding=utf-8

import ecs.component as component


# TODO game 上
class ComponentRecord(component.Component):
	def __init__(self):
		super(ComponentRecord, self).__init__(component.LABEL_RECORD)
		self.records = []
