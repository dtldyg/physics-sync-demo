# coding=utf-8

import time
import base.ecs as ecs


class SystemRenderLogic(ecs.System):
	def __init__(self):
		super(SystemRenderLogic, self).__init__((ecs.LABEL_TRANSFORM, ecs.LABEL_RENDER))
		self.roll_forward = True

	def update(self, dt, component_tuples):
		for _, comp_tuple in component_tuples:
			comp_transform, comp_render = comp_tuple
			comp_render.other_renders.clear()
			client_inter = comp_render.client_interpolation
			client_inter[0], client_inter[1] = client_inter[2], client_inter[3]
			client_inter[2], client_inter[3] = comp_transform.position, time.time()
