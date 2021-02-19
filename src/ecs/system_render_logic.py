# coding=utf-8

import time
import ecs.system as system
import ecs.component as component


class SystemRenderLogic(system.System):
	def __init__(self):
		super(SystemRenderLogic, self).__init__((component.LABEL_TRANSFORM, component.LABEL_RENDER))

	def update(self, dt, component_tuples):
		for _, component_tuple in component_tuples:
			component_transform, component_render = component_tuple
			component_render.other_renders.clear()
			client_interpolation = component_render.client_interpolation
			client_interpolation[0], client_interpolation[1] = client_interpolation[2], client_interpolation[3]
			client_interpolation[2], client_interpolation[3] = component_transform.position, time.time()
