# coding=utf-8

import base.math as math
import base.ecs as ecs
import base.const as const
import logic.component_connection as component_connection
import logic.component_package as component_package
import logic.component_physics as component_physics
import logic.component_frame as component_frame
import logic.component_transform as component_transform
import logic.component_render as component_render


class EntityPlayer(ecs.Entity):
	def __init__(self, eid, init_pos, send_q):
		super(EntityPlayer, self).__init__(eid)
		self.add_component(component_connection.ComponentConnection(send_q))
		self.add_component(component_package.ComponentPackage())
		self.add_component(component_physics.ComponentPhysics())
		self.add_component(component_frame.ComponentFrame())
		self.add_component(component_transform.ComponentTransform(math.Vector(*init_pos)))
		if const.SERVER_DO_RENDER:
			self.add_component(component_render.ComponentRender())
