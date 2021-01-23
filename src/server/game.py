# coding=utf-8

import time
import queue
import pygame

import common.const as const
import common.math as math
import server.entity as entity


class Game(object):
	def __init__(self, recv_q):
		self.entities = {}
		self.send_qs = {}
		self.recv_q = recv_q

	def run(self):
		clock = pygame.time.Clock()
		lt = time.time()

		while True:
			# input
			while True:
				try:
					pkg = self.recv_q.get_nowait()
				except queue.Empty:
					break
				client_id = pkg['id']
				if pkg['cmd'] == 'in':
					send_q = pkg['send_q']
					server_entity = entity.ServerEntity(client_id)
					self.send_qs[client_id] = send_q
					self.entities[client_id] = server_entity
					# broadcast
					del pkg['send_q']
					self.to_all(pkg)
				elif pkg['cmd'] == 'over':
					# broadcast
					self.to_all(pkg)
					del self.entities[client_id]
					del self.send_qs[client_id]
				elif pkg['cmd'] == 'sync':
					# broadcast
					self.to_all(pkg)
					server_entity = self.entities[client_id]
					server_entity.comp_state.pos = math.Vector(**pkg['p'])
					server_entity.comp_physics.velocity = math.Vector(**pkg['v'])

			# calc dt
			now = time.time()
			lt, dt = now, now - lt

			# update all entities
			for server_entity in self.entities.values():
				server_entity.update(dt)

			# output

			clock.tick(const.SERVER_FPS)

	def to_all(self, pkg):
		self.to_others('', pkg)

	def to_others(self, my_id, pkg):
		for client_id, send_q in self.send_qs.items():
			if client_id == my_id:
				continue
			send_q.put(pkg)


# game
def run_game(recv_q):
	Game(recv_q).run()
