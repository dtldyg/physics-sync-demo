# coding=utf-8

class System(object):
	def __init__(self, component_labels):
		self.world = None
		self.component_labels = component_labels
		self.component_label_mask = 0
		for label in component_labels:
			self.component_label_mask |= label

	def init(self, world):
		self.world = world

	def update(self, dt, component_tuples):
		pass
