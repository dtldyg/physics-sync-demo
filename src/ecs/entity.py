# coding=utf-8

class Entity(object):
	def __init__(self):
		self.eid = 0
		self.components = {}

	def add_component(self, component):
		self.components[component.label] = component

	def component_tuple(self, component_labels):
		return [self.components[label] for label in component_labels if label in self.components]
