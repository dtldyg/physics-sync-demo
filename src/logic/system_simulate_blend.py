# coding=utf-8

import base.ecs as ecs
import base.const as const


class SystemSimulateBlend(ecs.System):
	def __init__(self):
		super(SystemSimulateBlend, self).__init__((ecs.LABEL_PHYSICS, ecs.LABEL_TRANSFORM))

	def update(self, dt, component_tuples):
		master_eid = self.world.master_eid()
		for eid, comp_tuple in component_tuples:
			if eid == master_eid:
				continue
			comp_physics, comp_transform = comp_tuple
			if const.REPLICA_BEHAVIOR == const.REPLICA_PHYSIC_BLEND and comp_physics.blending:
				blend_ratio = 0
				for i in range(len(const.PHYSICS_BLEND_CURVE) - 1, -1, -1):
					sample1 = const.PHYSICS_BLEND_CURVE[i]
					if comp_physics.blend_time >= sample1[0]:
						if i == len(const.PHYSICS_BLEND_CURVE) - 1:
							comp_physics.blending = False
							comp_physics.blend_time = 0
						else:
							sample2 = const.PHYSICS_BLEND_CURVE[i + 1]
							blend_ratio = sample1[1] + (comp_physics.blend_time - sample1[0]) * (sample2[1] - sample1[1]) / (sample2[0] - sample1[0])
							comp_physics.blend_time += dt
						break
				position = comp_transform.position * blend_ratio + comp_transform.interpolation_position * (1 - blend_ratio)
				velocity = comp_transform.velocity * blend_ratio + comp_transform.interpolation_velocity * (1 - blend_ratio)
			else:
				position = comp_transform.interpolation_position
				velocity = comp_transform.interpolation_velocity
			comp_transform.position = position
			comp_transform.velocity = velocity
			comp_transform.modified = True
