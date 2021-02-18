# coding=utf-8

# label
LABEL_CONNECTION = 1 << 0
LABEL_PACKAGE = 1 << 1
LABEL_CONTROL = 1 << 2
LABEL_TRANSFORM = 1 << 3


class Component(object):
	def __init__(self, label):
		self.label = label
