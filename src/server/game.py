# coding=utf-8

import time
import queue
import pygame

import common.base.const as const
import common.net as net
import common.scene as scene

import server.entity as entity


def run_game():
	clock = pygame.time.Clock()
	logic_lt = time.time()
	states_lt = time.time()
	states_interval = 1 / const.NETWORK_STATES_FPS

	while True:
		# calc dt
		now = time.time()
		logic_lt, dt = now, now - logic_lt

		# recv
		for pkg in net.iter_recv_pkg():
			process_pkg(pkg)

		# update logic & physics
		scene.iter_entities(lambda e: e.update_logic(dt))
		scene.iter_entities(lambda e: e.update_physics(dt))

		# send states
		if now - states_lt >= states_interval:
			states_lt = now
			states = [e.output_state() for e in scene.get_all_entities()]
			for en in scene.get_all_entities():
				pkg = {'pid': net.PID_STATES, 'frame': en.frame, 'states': states}
				en.send_q.put(pkg)

		# fps limit
		clock.tick(const.LOGIC_FPS)


def to_all(pkg):
	scene.iter_entities(lambda e: e.send_q.put(pkg))


def process_pkg(pkg):
	if pkg['pid'] == net.PID_JOIN:
		en = entity.ServerEntity(pkg['send_q'])
		en.eid = pkg['eid']
		en.send_q.put({'pid': net.PID_ADD_MASTER, 'eid': en.eid})
		# broadcast
		to_all({'pid': net.PID_ADD_REPLICA, 'eid': en.eid})
		scene.add_entity(en)
	elif pkg['pid'] == net.PID_DEL:
		en = scene.get_entity(pkg['eid'])
		en.send_q.put(pkg)
		# broadcast
		scene.del_entity(en.eid)
		to_all({'pid': net.PID_DEL_REPLICA, 'eid': en.eid})
	elif pkg['pid'] == net.PID_CMD:
		en = scene.get_entity(pkg['eid'])
		en.recv_cmd(pkg)
