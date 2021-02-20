# coding=utf-8

import base.ecs as ecs
import logic.component_package as component_package
import logic.component_physics as component_physics
import logic.component_transform as component_transform
import logic.component_render as component_render


class EntityPlayerReplica(ecs.Entity):
	def __init__(self, eid):
		super(EntityPlayerReplica, self).__init__(eid)
		self.add_component(component_package.ComponentPackage())
		self.add_component(component_physics.ComponentPhysics())
		self.add_component(component_transform.ComponentTransform())
		self.add_component(component_render.ComponentRender())