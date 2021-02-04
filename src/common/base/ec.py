# coding=utf-8


class Entity(object):
	def __init__(self):
		self.eid = -1
		self.frame = -1
		self.comps = []

	def update_logic(self, dt):
		self.frame = self.frame + 1
		self.iter_comps(lambda c: c.update_logic(dt))

	def update_physics(self, dt):
		self.iter_comps(lambda c: c.update_physics(dt))

	def update_render(self, dt):
		self.iter_comps(lambda c: c.update_render(dt))

	def add_comp(self, comp):
		comp.entity = self
		comp.init()
		self.comps.append(comp)

	def get_comp(self, name):
		return [c for c in self.comps if c.name == name][0]

	def iter_comps(self, f):
		for comp in self.comps:
			f(comp)


class Component(object):
	def __init__(self, name):
		self.name = name
		self.entity = None

	def init(self):
		pass

	def update_logic(self, dt):
		pass

	def update_physics(self, dt):
		pass

	def update_render(self, dt):
		pass
