# coding=utf-8

import base.ecs as ecs


class ComponentConnection(ecs.Component):
	def __init__(self, send_q):
		super(ComponentConnection, self).__init__(ecs.LABEL_CONNECTION)
		self.send_q = send_q
