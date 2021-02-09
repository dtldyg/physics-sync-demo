# coding=utf-8

import common.base.const as const
import ecs.system_net_in as system_net_in
import ecs.system_control as system_control
import ecs.system_physics as system_physics
import ecs.system_net_out as system_net_out


class World(object):
	def __init__(self):
		if const.IS_CLIENT:
			self.systems = []
		else:
			self.systems = [
				system_net_in.SystemNetIn(),
				system_control.SystemControl(),
				system_physics.SystemPhysics(),
				system_net_out.SystemNetOut(),
			]
		self.entities = []

	def update(self, dt):
		for s in self.systems:
			component_tuples = []
			for e in self.entities:
				t = e.component_tuple(s.component_labels)
				if len(t) > 0:
					component_tuples.append((e.eid, t))
			s.update(dt, component_tuples)
