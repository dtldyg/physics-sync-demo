# coding=utf-8

import base.ecs as ecs


# 内插：抛物线插值
class SystemParabolicSpline(ecs.System):
	def __init__(self):
		super(SystemParabolicSpline, self).__init__((ecs.LABEL_TRANSFORM,))

	def update(self, dt, component_tuples):
		# 外插：航位推算
		master_eid = self.world.master_eid()
		for eid, comp_tuple in component_tuples:
			if eid == master_eid:
				continue
			comp_transform, = comp_tuple
