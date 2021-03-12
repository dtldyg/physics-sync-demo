# coding=utf-8

import base.ecs as ecs


class SystemReset(ecs.System):
	def __init__(self):
		super(SystemReset, self).__init__((ecs.LABEL_TRANSFORM, ecs.LABEL_RENDER))

	def update(self, dt, component_tuples):
		for _, comp_tuple in component_tuples:
			comp_transform, comp_render = comp_tuple
			comp_transform.modified = False
			comp_transform.server_modified = False
			comp_render.other_renders.clear()
