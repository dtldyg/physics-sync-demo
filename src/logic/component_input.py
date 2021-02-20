# coding=utf-8

import base.ecs as ecs


class ComponentInput(ecs.Component):
	def __init__(self):
		super(ComponentInput, self).__init__(ecs.LABEL_INPUT)
		self.key_down = set()  # key
		self.mouse_state = {}  # {'active': False, 'trigger_down': set(key), 'trigger_up':set(key)}
