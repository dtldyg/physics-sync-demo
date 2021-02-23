# coding=utf-8

import base.ecs as ecs


class SystemModifiedReset(ecs.System):
	def __init__(self):
		super(SystemModifiedReset, self).__init__((ecs.LABEL_TRANSFORM,))

	def update(self, dt, component_tuples):
		for _, comp_tuple in component_tuples:
			comp_transform, = comp_tuple
			comp_transform.modified = False
			comp_transform.server_modified = False
