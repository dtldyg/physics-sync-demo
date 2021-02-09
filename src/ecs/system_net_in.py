# coding=utf-8

import common.net as net
import ecs.system as system
import ecs.component as component
import ecs.entity_player as entity_player


class SystemNetIn(system.System):
	def __init__(self):
		super(SystemNetIn, self).__init__((component.LABEL_NET,))

	def update(self, dt, component_tuples):
		component_tuple_dict = {}
		for eid, component_tuple in component_tuples:
			component_tuple_dict[eid] = component_tuple

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
