# coding=utf-8

import ecs.component as component


class ComponentGlobal(component.Component):
	def __init__(self):
		super(ComponentGlobal, self).__init__(component.LABEL_GLOBAL)
		self.master_entity_id = 0
