# coding=utf-8

import base.ecs as ecs


# 外插：航位推算
class SystemExtrapolation(ecs.System):
	def __init__(self):
		super(SystemExtrapolation, self).__init__((ecs.LABEL_TRANSFORM,))

	def update(self, dt, component_tuples):
		master_eid = self.world.master_eid()
		for eid, comp_tuple in component_tuples:
			if eid == master_eid:
				continue
			comp_transform, = comp_tuple
