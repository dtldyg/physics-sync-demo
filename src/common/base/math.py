# coding=utf-8


class Vector(object):
	def __init__(self, x=0, y=0):
		self.x, self.y = x, y

	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y)

	def __mul__(self, other):
		return Vector(self.x * other, self.y * other)

	def __truediv__(self, other):
		return Vector(self.x / other, self.y / other)

	def __eq__(self, other):
		return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9

	def __ne__(self, other):
		return not self == other

	def __repr__(self):
		return '({},{})'.format(self.x, self.y)

	def tuple(self):
		return self.x, self.y

	def length(self):
		return (self.x ** 2 + self.y ** 2) ** 0.5

	def zero(self):
		return abs(self.x) < 1e-6 and abs(self.y) < 1e-6

	def normal(self):
		length = self.length()
		if length > 0:
			return Vector(self.x / length, self.y / length)
		else:
			return vector_zero


vector_zero = Vector()
