# coding=utf-8

import common.base.math as math
import server.entity as ec


class CompControl(ec.ServerComponent):
	def __init__(self):
		super(CompControl, self).__init__('comp_control')
		# TODO 这里做帧缓冲，update_logic里取0,1,2更新
		pass

	def input_cmd(self, pkg):
		comp_physics = self.entity.get_comp('comp_physics')
		comp_physics.f = math.Vector(**pkg['f'])
