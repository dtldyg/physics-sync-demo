# coding=utf-8

import base.ecs as ecs


class ComponentPackage(ecs.Component):
	def __init__(self):
		super(ComponentPackage, self).__init__(ecs.LABEL_PACKAGE)
		self.packages = []
