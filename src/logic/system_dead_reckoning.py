# coding=utf-8

import base.ecs as ecs


class SystemDeadReckoning(ecs.System):
	def __init__(self):
		super(SystemDeadReckoning, self).__init__((ecs.LABEL_TRANSFORM,))

	def update(self, dt, component_tuples):
		for eid, comp_tuple in component_tuples:
			comp_transform, = comp_tuple
