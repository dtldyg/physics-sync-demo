# coding=utf-8

import base.const as const
import base.ecs as ecs


class SystemInterpolation(ecs.System):
	def __init__(self):
		super(SystemInterpolation, self).__init__((ecs.LABEL_TRANSFORM, ecs.LABEL_INTERPOLATION))

	def update(self, dt, component_tuples):
		for eid, comp_tuple in component_tuples:
			is_master = eid == self.world.master_eid()
			if is_master:
				if const.MASTER_BEHAVIOR != const.MASTER_INTERPOLATION:
					continue
			else:
				if const.REPLICA_BEHAVIOR != const.REPLICA_INTERPOLATION and const.REPLICA_BEHAVIOR != const.REPLICA_PHYSIC_BLEND:
					continue
			comp_transform, comp_interpolation = comp_tuple
			target_velocity = comp_transform.server_velocity
			target_position = comp_transform.server_position
			if comp_transform.server_modified:
				comp_interpolation.mode = const.REPLICA_INTERPOLATION_LINEAR if is_master else const.REPLICA_INTERPOLATION_MODE
				comp_interpolation.pass_t = 0
				comp_interpolation.remain_t = 1 / const.STATES_FPS
				if comp_interpolation.mode == const.REPLICA_INTERPOLATION_LINEAR:
					pass
				elif comp_interpolation.mode == const.REPLICA_INTERPOLATION_CUBIC:
					t = comp_interpolation.remain_t
					h = target_position - comp_transform.position
					comp_interpolation.cubic_args[0] = comp_transform.position
					comp_interpolation.cubic_args[1] = comp_transform.velocity
					comp_interpolation.cubic_args[2] = (h * 3 - (comp_transform.velocity * 2 + target_velocity) * t) / (t ** 2)
					comp_interpolation.cubic_args[3] = (h * -2 + (comp_transform.velocity + target_velocity) * t) / (t ** 3)
			# https://zhuanlan.zhihu.com/p/269230598
			if comp_interpolation.remain_t <= dt:
				comp_transform.position = target_position
			else:
				if comp_interpolation.mode == const.REPLICA_INTERPOLATION_LINEAR:
					# 线性插值: 位置:连续, 速度:突变, 加速度:恒0
					# p(t) = p0 + (p1 - p0) / (t1 - t0) * (t - t0)
					comp_transform.velocity = (target_position - comp_transform.position) / comp_interpolation.remain_t
					comp_transform.position = comp_transform.position + comp_transform.velocity * dt
				elif comp_interpolation.mode == const.REPLICA_INTERPOLATION_CUBIC:
					# 三次插值: 位置:平滑, 速度:平滑, 加速度:连续
					# p(t) = a0 + a1 * (t - t0) + a2 * (t - t0)^2 + a3 * (t - t0)^3
					a0, a1, a2, a3 = comp_interpolation.cubic_args
					t = comp_interpolation.pass_t + dt
					comp_transform.velocity = a1 + a2 * 2 * t + a3 * 3 * t ** 2
					comp_transform.position = a0 + a1 * t + a2 * t ** 2 + a3 * t ** 3
			comp_interpolation.pass_t += dt
			comp_interpolation.remain_t -= dt
			comp_transform.modified = True
