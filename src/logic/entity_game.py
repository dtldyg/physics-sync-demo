# coding=utf-8

import base.const as const
import base.ecs as ecs
import logic.component_package as component_package
import logic.component_surface as component_surface
import logic.component_gui as component_gui
import logic.component_info as component_info
import logic.component_input as component_input
import logic.component_record as component_record


# global single entity
class EntityGame(ecs.Entity):
	def __init__(self):
		super(EntityGame, self).__init__(const.ENTITY_GAME_ID)
		self.add_component(component_package.ComponentPackage())
		if const.IS_CLIENT:
			self.add_component(component_surface.ComponentSurface())
			self.add_component(component_gui.ComponentGUI())
			self.add_component(component_info.ComponentInfo())
			self.add_component(component_input.ComponentInput())
			self.add_component(component_record.ComponentRecord())
