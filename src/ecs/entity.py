# coding=utf-8

class Entity(object):
	def __init__(self, eid):
		self.eid = eid
		self.components = {}
		self.component_label_mask = 0

	def add_component(self, component):
		self.components[component.label] = component
		self.component_label_mask |= component.label

	def component_tuple(self, component_labels, component_label_mask):
		if self.component_label_mask & component_label_mask != component_label_mask:
			return None
		return tuple([self.components[label] for label in component_labels])
