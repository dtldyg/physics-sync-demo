# coding=utf-8

import time
import queue
import pygame

import common.const as const
import common.scene as scene

import server.io as io
import server.entity as entity


def run_game():
	print('game run')

	clock = pygame.time.Clock()
	lt = time.time()

	while True:
		# calc dt
		now = time.time()
		lt, dt = now, now - lt

		# io in
		while True:
			try:
				pkg = io.recv_q.get_nowait()
			except queue.Empty:
				break
			cmd = pkg['cmd']
			if cmd == 'new':
				cmd_new(pkg)
			elif cmd == 'del':
				cmd_del(pkg)
			else:
				scene.iter_entities(lambda e: e.io_in(pkg))

		# update logic
		scene.iter_entities(lambda e: e.update_logic(dt))
		# update physics
		scene.iter_entities(lambda e: e.update_physics(dt))

		# io out
		scene.iter_entities(lambda e: e.io_out())

		# fps limit
		clock.tick(const.SERVER_FPS)


def to_all(pkg):
	scene.iter_entities(lambda e: e.send_q.put(pkg))


def to_others(client_id, pkg):
	for e in scene.get_all_entities():
		if e.client_id == client_id:
			continue
		e.send_q.put(pkg)


def cmd_new(pkg):
	server_entity = entity.ServerEntity(pkg['id'], pkg['send_q'])
	scene.add_entity(server_entity)
	# broadcast
	del pkg['send_q']
	to_all(pkg)


def cmd_del(pkg):
	eids = [e.eid for e in scene.get_all_entities() if e.client_id == pkg['id']]
	scene.del_entities(eids)
	# broadcast
	to_all(pkg)
