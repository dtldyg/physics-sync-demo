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

	def add_comp(self, comp):
		comp.entity = self
		comp.init()
		self.comps.append(comp)

	def get_comp(self, name):
		for comp in self.comps:
			if comp.name == name:
				return comp
		return None

	def iter_comps(self, f):
		for comp in self.comps:
			f(comp)


class ClientEntity(Entity):
	def update_render(self, dt):
		self.iter_comps(lambda c: c.update_render(dt))

	# send cmd to server (only master entity)
	def send_cmd(self):
		cmd = {'eid': self.eid}
		self.iter_comps(lambda c: c.send_cmd(cmd))
		return cmd

	# recv state from server
	def recv_state(self, state):
		self.iter_comps(lambda c: c.recv_state(state))


class ServerEntity(Entity):
	# recv cmd from client
	def recv_cmd(self, cmd):
		self.iter_comps(lambda c: c.recv_cmd(cmd))

	# send state to client
	def send_state(self):
		state = {'eid': self.eid}
		self.iter_comps(lambda c: c.send_state(state))
		return state


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


class ClientComponent(Component):
	def send_cmd(self, cmd):
		pass

	def recv_state(self, state):
		pass


class ServerComponent(Component):
	def recv_cmd(self, cmd):
		pass

	def send_state(self, state):
		pass
