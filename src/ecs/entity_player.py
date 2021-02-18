# coding=utf-8

import common.base.math as math
import common.base.const as const
import ecs.component_connection as component_net
import ecs.component_package as component_package
import ecs.component_control as component_control
import ecs.component_transform as component_transform
import ecs.entity as entity


class EntityPlayer(entity.Entity):
	def __init__(self, send_q):
		super(EntityPlayer, self).__init__()
		self.add_component(component_net.ComponentConnection(send_q))
		self.add_component(component_package.ComponentPackage())
		self.add_component(component_control.ComponentControl())
		self.add_component(component_transform.ComponentTransform(math.Vector(*const.MASTER_INIT_POS)))
