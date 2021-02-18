# coding=utf-8

import ecs.component as component


class ComponentPackage(component.Component):
	def __init__(self):
		super(ComponentPackage, self).__init__(component.LABEL_PACKAGE)
		self.packages = []
