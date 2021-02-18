# coding=utf-8

import ecs.component_package as component_package
import ecs.entity as entity


class EntityGame(entity.Entity):
	def __init__(self):
		super(EntityGame, self).__init__()
		self.add_component(component_package.ComponentPackage())
