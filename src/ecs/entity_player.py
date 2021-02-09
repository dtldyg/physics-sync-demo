# coding=utf-8

import ecs.component_net as component_net
import ecs.component_control as component_control
import ecs.component_transform as component_transform
import ecs.entity as entity


class EntityPlayer(entity.Entity):
	def __init__(self):
		super(EntityPlayer, self).__init__()
		self.add_component(component_net.ComponentNet())
		self.add_component(component_control.ComponentControl())
		self.add_component(component_transform.ComponentTransform())
