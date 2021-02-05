# coding=utf-8

import time

import common.base.const as const
import common.base.clock as clock
import common.net as net
import common.scene as scene

import server.entity as entity


def run_game():
	c = clock.Clock()
	c.add(const.LOGIC_FPS, tick_logic)
	c.add(const.STATES_FPS, tick_state)
	print('game run')
	c.run()


def tick_logic(dt):
	# recv cmd
	for pkg in net.iter_recv_pkg():
		if pkg['pid'] == net.PID_JOIN:
			en = entity.ServerEntity(pkg['send_q'])
			en.eid = pkg['eid']
			state = en.send_state()
			en.send_q.put({'pid': net.PID_ADD_MASTER, 'state': state})
			# broadcast
			scene.iter_entities(lambda e: e.send_q.put({'pid': net.PID_ADD_REPLICA, 'state': state}))
			scene.add_entity(en)
			print('join:', en.eid)
		elif pkg['pid'] == net.PID_DEL:
			en = scene.get_entity(pkg['eid'])
			en.send_q.put(pkg)
			# broadcast
			scene.del_entity(en.eid)
			scene.iter_entities(lambda e: e.send_q.put({'pid': net.PID_DEL_REPLICA, 'eid': en.eid}))
			print('del:', en.eid)
		elif pkg['pid'] == net.PID_CMD:
			en = scene.get_entity(pkg['eid'])
			en.recv_cmd(pkg)

	# update logic & physics
	scene.iter_entities(lambda e: e.update_logic(dt))
	scene.iter_entities(lambda e: e.update_physics(dt))


def tick_state(dt):
	# send states
	states = [e.send_state() for e in scene.get_all_entities()]
	for en in scene.get_all_entities():
		pkg = {'pid': net.PID_STATES, 'frame': en.frame, 'states': states}
		en.send_q.put(pkg)
