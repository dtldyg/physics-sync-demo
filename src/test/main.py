# coding=utf-8

class Vector(object):
	def __init__(self, x=0, y=0):
		self.x, self.y = x, y


f = {'x': 1, 'y': 2}
v = Vector(**f)
print(v.x, v.y)
