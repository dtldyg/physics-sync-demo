# coding=utf-8


class Entity(object):
	def __init__(self, flags):
		self.entity_flags = 0
		for flag in flags:
			if flag[1] == 1:
				self.entity_flags = self.entity_flags | flag[0]
		self.comps = []

	def io_in(self, pkg):
		self.iter_comps(lambda c: c.io_in(pkg))

	def update_logic(self, dt):
		self.iter_comps(lambda c: c.update_logic(dt))

	def update_physics(self, dt):
		self.iter_comps(lambda c: c.update_physics(dt))

	def update_render(self, dt):
		self.iter_comps(lambda c: c.update_render(dt))

	def io_out(self):
		self.iter_comps(lambda c: c.io_out())

	def add_comp(self, comp):
		comp.entity = self
		comp.init()
		self.comps.append(comp)

	def get_comp(self, name):
		return [c for c in self.comps if c.name == name][0]

	def iter_comps(self, f):
		for comp in self.comps:
			f(comp)

	def has_flags(self, *flags):
		for flag in flags:
			if self.entity_flags & flag[0] != flag[0] * flag[1]:
				return False
		return True


class Component(object):
	def __init__(self, name):
		self.name = name
		self.entity = None

	def init(self):
		pass

	def io_in(self, pkg):
		pass

	def update_logic(self, dt):
		pass

	def update_physics(self, dt):
		pass

	def update_render(self, dt):
		pass

	def io_out(self):
		pass
