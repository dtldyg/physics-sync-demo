# coding=utf-8

import ecs.component_package as component_package
import ecs.component_physics as component_physics
import ecs.component_transform as component_transform
import ecs.component_render as component_render
import ecs.entity as entity


class EntityPlayerReplica(entity.Entity):
	def __init__(self, eid):
		super(EntityPlayerReplica, self).__init__(eid)
		self.add_component(component_package.ComponentPackage())
		self.add_component(component_physics.ComponentPhysics())
		self.add_component(component_transform.ComponentTransform())
		self.add_component(component_render.ComponentRender())
