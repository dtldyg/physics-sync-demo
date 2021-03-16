# coding=utf-8

import time
import base.ecs as ecs


class SystemRenderLogic(ecs.System):
	def __init__(self):
		super(SystemRenderLogic, self).__init__((ecs.LABEL_TRANSFORM, ecs.LABEL_RENDER))
		self.roll_forward = True

	def update(self, dt, component_tuples):
		game_comp_info = self.world.game_component(ecs.LABEL_INFO)
		game_comp_info.logic_fps += 1
		for _, comp_tuple in component_tuples:
			comp_transform, comp_render = comp_tuple
			# interpolation
			if comp_transform.modified:
				interpolation = comp_render.interpolation
				interpolation[0], interpolation[1] = interpolation[2], interpolation[3]
				interpolation[2], interpolation[3] = comp_transform.position, time.time()
