# coding=utf-8

import ecs.component as component


# TODO player_master 上
class ComponentControl(component.Component):
	def __init__(self):
		super(ComponentControl, self).__init__(component.LABEL_CONTROL)
		self.line_stage = 0  # 0:none 1:draw 2:wait 3:trigger
		self.line_start = None
		self.line_end = None
		self.line_f_dir = None
		self.line_t = 0
