# coding=utf-8

import common.base.const as const
import ecs.component_package as component_package
import ecs.component_surface as component_surface
import ecs.component_global as component_global
import ecs.entity as entity


# global single entity
class EntityGame(entity.Entity):
	def __init__(self):
		super(EntityGame, self).__init__(const.ENTITY_GAME_ID)
		if const.IS_CLIENT:
			self.add_component(component_global.ComponentGlobal())
			self.add_component(component_surface.ComponentSurface())
		self.add_component(component_package.ComponentPackage())
