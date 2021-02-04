# coding=utf-8

import time
import queue
import pygame

import common.base.const as const
import common.net as net
import common.scene as scene

import server.ec as entity


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
			if pkg['pid'] == net.PID_JOIN:
				server_entity = entity.ServerEntity(pkg['send_q'])
				server_entity.eid = pkg['eid']
				server_entity.send_q.put({'pid': net.PID_ADD_MASTER, 'eid': server_entity.eid})
				# broadcast
				to_all({'pid': net.PID_ADD_REPLICA, 'eid': server_entity.eid})
				scene.add_entity(server_entity)
			elif pkg['pid'] == net.PID_DEL:
				server_entity = scene.get_entity(pkg['eid'])
				server_entity.send_q.put(pkg)
				# broadcast
				scene.del_entity(server_entity.eid)
				to_all({'pid': net.PID_DEL_REPLICA, 'eid': server_entity.eid})
			elif pkg['pid'] == net.PID_CMD:
				server_entity = scene.get_entity(pkg['eid'])
				server_entity.input_cmd(pkg)

		# update logic & physics
		scene.iter_entities(lambda e: e.update_logic(dt))
		scene.iter_entities(lambda e: e.update_physics(dt))

		# send states
		if now - states_lt >= states_interval:
			states_lt = now
			states = [e.output_state() for e in scene.get_all_entities()]
			for e in scene.get_all_entities():
				pkg = {'pid': net.PID_STATES, 'frame': e.frame, 'states': states}
				e.send_q.put(pkg)

		# fps limit
		clock.tick(const.LOGIC_FPS)


def to_all(pkg):
	scene.iter_entities(lambda e: e.send_q.put(pkg))
