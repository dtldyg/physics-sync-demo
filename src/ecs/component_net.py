# coding=utf-8

import common.base.const as const
import ecs.component as component


class ComponentNet(component.Component):
	def __init__(self):
		super(ComponentNet, self).__init__(component.LABEL_NET)
		self.in_packages = []
		self.out_packages = []
		if const.IS_SERVER:
			self.send_q = None
