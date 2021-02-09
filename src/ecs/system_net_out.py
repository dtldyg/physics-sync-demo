# coding=utf-8

import ecs.system as system
import ecs.component as component


class SystemNetOut(system.System):
	def __init__(self):
		super(SystemNetOut, self).__init__((component.LABEL_TRANSFORM,))
