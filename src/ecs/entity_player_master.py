# coding=utf-8

import ecs.component_package as component_package
import ecs.component_input as component_input
import ecs.component_control as component_control
import ecs.component_physics as component_physics
import ecs.component_transform as component_transform
import ecs.component_render as component_render
import ecs.component_record as component_record
import ecs.entity as entity


class EntityPlayerMaster(entity.Entity):
	def __init__(self, eid):
		super(EntityPlayerMaster, self).__init__(eid)
		self.add_component(component_package.ComponentPackage())
		self.add_component(component_input.ComponentInput())
		self.add_component(component_control.ComponentControl())
		self.add_component(component_physics.ComponentPhysics())
		self.add_component(component_transform.ComponentTransform())
		self.add_component(component_render.ComponentRender())
		self.add_component(component_record.ComponentRecord())
