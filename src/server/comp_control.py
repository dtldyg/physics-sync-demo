# coding=utf-8

import common.base.math as math
import common.base.const as const
import common.ec as ec


class CompControl(ec.ServerComponent):
	def __init__(self):
		super(CompControl, self).__init__('comp_control')
		# TODO 这里做帧缓冲，update_logic里取0,1,2更新
		pass

	def recv_cmd(self, cmd):
		comp_physics = self.entity.get_comp('comp_physics')
		if cmd['f']['x'] == 0 and cmd['f']['y'] == 0:
			comp_physics.f = math.vector_zero
		else:
			comp_physics.f = math.Vector(**cmd['f']).normal() * const.ENTITY_FORCE
