# coding=utf-8

import common.physics as physics
import ecs.system as system
import ecs.component as component


class SystemPhysics(system.System):
	def __init__(self):
		super(SystemPhysics, self).__init__((component.LABEL_CONTROL, component.LABEL_TRANSFORM))

	def update(self, dt, component_tuples):
		# move
		for _, component_tuple in component_tuples:
			component_control, component_transform = component_tuple
			f = component_control.force_normal
			p, v = component_transform.position, component_transform.velocity
			component_transform.position, component_transform.velocity = physics.pv_with_force_normal(p, v, f, dt)
		# collision
		for _, component_tuple in component_tuples:
			_, component_transform = component_tuple
			p, v = component_transform.position, component_transform.velocity
			component_transform.position, component_transform.velocity = physics.pv_with_wall(p, v, dt)
