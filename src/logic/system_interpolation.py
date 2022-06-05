# coding=utf-8

import base.const as const
import base.ecs as ecs


class SystemInterpolation(ecs.System):
	def __init__(self, world):
		super(SystemInterpolation, self).__init__(world, (ecs.LABEL_TRANSFORM, ecs.LABEL_INTERPOLATION))
		self.roll_forward = True

	def update(self, dt, component_tuples):
		master_eid = self.world.master_eid()
		for eid, comp_tuple in component_tuples:
			is_master = eid == master_eid
			if is_master:
				if const.MASTER_BEHAVIOR != const.MASTER_INTERPOLATION:
					continue
			else:
				if const.REPLICA_BEHAVIOR == const.REPLICA_NONE:
					continue
			comp_transform, comp_interpolation = comp_tuple
			target_velocity = comp_transform.server_velocity
			target_position = comp_transform.server_position
			if not is_master and (const.REPLICA_BEHAVIOR == const.REPLICA_EXTRAPOLATION or const.REPLICA_BEHAVIOR == const.REPLICA_PHYSIC_BLEND):
				target_velocity = comp_transform.extrapolation_velocity
				target_position = comp_transform.extrapolation_position
			# re-calc interpolation params
			if comp_transform.server_modified:
				comp_interpolation.mode = const.INTERPOLATION_MODE_LINEAR if is_master else const.REPLICA_INTERPOLATION_MODE
				comp_interpolation.pass_t = 0
				comp_interpolation.remain_t = 1 / const.STATES_FPS
				if comp_interpolation.mode == const.INTERPOLATION_MODE_LINEAR:
					pass
				elif comp_interpolation.mode == const.INTERPOLATION_MODE_CUBIC:
					t = comp_interpolation.remain_t
					h = target_position - comp_transform.interpolation_position
					comp_interpolation.cubic_args[0] = comp_transform.interpolation_position
					comp_interpolation.cubic_args[1] = comp_transform.interpolation_velocity
					comp_interpolation.cubic_args[2] = (h * 3 - (comp_transform.interpolation_velocity * 2 + target_velocity) * t) / (t ** 2)
					comp_interpolation.cubic_args[3] = (h * -2 + (comp_transform.interpolation_velocity + target_velocity) * t) / (t ** 3)
			# do interpolation
			# https://zhuanlan.zhihu.com/p/269230598
			if comp_interpolation.remain_t <= dt:
				velocity = target_velocity
				position = target_position
			else:
				if comp_interpolation.mode == const.INTERPOLATION_MODE_LINEAR:
					# 线性插值: 位置:连续, 速度:突变, 加速度:恒0
					# p(t) = p0 + (p1 - p0) / (t1 - t0) * (t - t0)
					velocity = (target_position - comp_transform.interpolation_position) / comp_interpolation.remain_t
					position = comp_transform.interpolation_position + velocity * dt
				else:
					# 三次插值: 位置:平滑, 速度:平滑, 加速度:连续
					# p(t) = a0 + a1 * (t - t0) + a2 * (t - t0)^2 + a3 * (t - t0)^3
					a0, a1, a2, a3 = comp_interpolation.cubic_args
					t = comp_interpolation.pass_t + dt
					velocity = a1 + a2 * 2 * t + a3 * 3 * t ** 2
					position = a0 + a1 * t + a2 * t ** 2 + a3 * t ** 3
			comp_interpolation.pass_t += dt
			comp_interpolation.remain_t -= dt
			comp_transform.interpolation_velocity = velocity
			comp_transform.interpolation_position = position
