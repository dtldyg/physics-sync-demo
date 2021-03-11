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

	def __neg__(self):
		return Vector(-self.x, -self.y)

	def __eq__(self, other):
		return abs(self.x - other.x) < 1e-6 and abs(self.y - other.y) < 1e-6

	def __ne__(self, other):
		return not self == other

	def __repr__(self):
		return '({},{})'.format(self.x, self.y)

	def dot(self, other):
		return self.x * other.x + self.y * other.y

	def tuple(self):
		return self.x, self.y

	def dict(self):
		return self.__dict__

	def length(self):
		return (self.x ** 2 + self.y ** 2) ** 0.5

	def length_sqr(self):
		return self.x ** 2 + self.y ** 2

	def zero(self):
		return abs(self.x) < 1e-6 and abs(self.y) < 1e-6

	def near(self, other, margin=0.1):
		return abs(self.x - other.x) < margin and abs(self.y - other.y) < margin

	def normal(self):
		length = self.length()
		if length > 0:
			return Vector(self.x / length, self.y / length)
		else:
			return vector_zero


vector_zero = Vector()
