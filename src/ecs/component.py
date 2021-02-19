# coding=utf-8

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
LABEL_GLOBAL = 1 << 12


class Component(object):
	def __init__(self, label):
		self.label = label
