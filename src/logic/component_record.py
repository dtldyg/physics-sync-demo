# coding=utf-8

import base.ecs as ecs


class ComponentRecord(ecs.Component):
	def __init__(self):
		super(ComponentRecord, self).__init__(ecs.LABEL_RECORD)
		self.rollback = False
		self.rollback_notify = False
		self.records = []
