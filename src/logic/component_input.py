# coding=utf-8

import base.ecs as ecs


class ComponentInput(ecs.Component):
	def __init__(self):
		super(ComponentInput, self).__init__(ecs.LABEL_INPUT)
		self.key_down = set()
		self.mouse_state = {'active': False, 'trigger_down': set(), 'trigger_up': set()}
