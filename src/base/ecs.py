# coding=utf-8


class Entity(object):
	def __init__(self, eid):
		self.eid = eid
		self.components = {}
		self.component_label_mask = 0

	def add_component(self, component):
		self.components[component.label] = component
		self.component_label_mask |= component.label

	def get_component(self, component_label):
		return self.components[component_label]

	def component_tuple(self, component_labels, component_label_mask):
		if (self.component_label_mask & component_label_mask) != component_label_mask:
			return None
		return tuple([self.components[label] for label in component_labels])


# label
LABEL_CONNECTION = 1 << 0
LABEL_PACKAGE = 1 << 1
LABEL_PHYSICS = 1 << 2
LABEL_TRANSFORM = 1 << 3
LABEL_FRAME = 1 << 4
LABEL_CONTROL = 1 << 5
LABEL_INPUT = 1 << 6
LABEL_GUI = 1 << 7
LABEL_RENDER = 1 << 8
LABEL_RECORD = 1 << 9
LABEL_SURFACE = 1 << 10
LABEL_INFO = 1 << 11
LABEL_INTERPOLATION = 1 << 12


class Component(object):
	def __init__(self, label):
		self.label = label


class System(object):
	def __init__(self, component_labels):
		self.world = None
		self.roll_forward = False
		self.component_labels = component_labels
		self.component_label_mask = 0
		for label in component_labels:
			self.component_label_mask |= label

	def init(self, world):
		self.world = world

	def update(self, dt, component_tuples):
		pass
