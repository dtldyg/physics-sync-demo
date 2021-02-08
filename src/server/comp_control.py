# coding=utf-8

import common.base.math as math
import common.ec as ec


class CompControl(ec.ServerComponent):
	def __init__(self):
		super(CompControl, self).__init__('comp_control')
		self.f_nor = math.vector_zero

	def recv_cmd(self, cmd):
		# TODO 目前等于使用上一帧
		self.entity.frame = cmd['fr']
		if cmd['f']['x'] == 0 and cmd['f']['y'] == 0:
			self.f_nor = math.vector_zero
		else:
			self.f_nor = math.Vector(**cmd['f']).normal()
