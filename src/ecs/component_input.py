# coding=utf-8

import ecs.component as component


# TODO game 上
class ComponentInput(component.Component):
	def __init__(self):
		super(ComponentInput, self).__init__(component.LABEL_INPUT)
		self.key_down = set()  # key
		self.mouse_state = {}  # {'active': False, 'trigger_down': set(key), 'trigger_up':set(key)}
