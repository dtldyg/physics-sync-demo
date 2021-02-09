# coding=utf-8

# label
LABEL_CONTROL = 1
LABEL_NET = 2
LABEL_TRANSFORM = 3


class Component(object):
	def __init__(self, label):
		self.label = label
