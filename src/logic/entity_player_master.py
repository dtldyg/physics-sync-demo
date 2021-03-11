# coding=utf-8

import base.ecs as ecs
import logic.component_package as component_package
import logic.component_control as component_control
import logic.component_frame as component_frame
import logic.component_physics as component_physics
import logic.component_transform as component_transform
import logic.component_render as component_render


class EntityPlayerMaster(ecs.Entity):
	def __init__(self, eid, pos):
		super(EntityPlayerMaster, self).__init__(eid)
		self.add_component(component_package.ComponentPackage())
		self.add_component(component_control.ComponentControl())
		self.add_component(component_frame.ComponentFrame())
		self.add_component(component_physics.ComponentPhysics())
		self.add_component(component_transform.ComponentTransform(pos))
		self.add_component(component_render.ComponentRender(True))
