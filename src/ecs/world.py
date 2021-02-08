# coding=utf-8

class World(object):
	def __init__(self):
		self.systems = []
		self.entities = []

	def run(self):
		pass

	def update(self, dt):
		for s in self.systems:
			s.update(dt)
