# coding=utf-8

import base.ecs as ecs


class SystemPhysicsBlending(ecs.System):
	def __init__(self):
		super(SystemPhysicsBlending, self).__init__((ecs.LABEL_TRANSFORM,))

	def update(self, dt, component_tuples):
		pass
