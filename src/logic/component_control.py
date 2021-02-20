# coding=utf-8

import base.ecs as ecs


class ComponentControl(ecs.Component):
	def __init__(self):
		super(ComponentControl, self).__init__(ecs.LABEL_CONTROL)
		self.line_stage = 0  # 0:none 1:draw 2:wait 3:trigger
		self.line_start = None
		self.line_end = None
		self.line_f_dir = None
		self.line_t = 0
