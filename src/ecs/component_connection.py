# coding=utf-8

import ecs.component as component


class ComponentConnection(component.Component):
	def __init__(self, send_q):
		super(ComponentConnection, self).__init__(component.LABEL_CONNECTION)
		self.send_q = send_q
