# coding=utf-8

import ecs.system as system
import ecs.component as component


class SystemControl(system.System):
	def __init__(self, world):
		super(SystemControl, self).__init__(world, (component.LABEL_NET, component.LABEL_CONTROL))

	def update(self, dt, component_tuples):
		# 响应全局消息，分发entity消息到对应component_net中
		for eid, component_tuple in component_tuples:
			pass
