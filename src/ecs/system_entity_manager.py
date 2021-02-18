# coding=utf-8

import common.base.const as const
import common.net as net
import ecs.system as system
import ecs.component as component
import ecs.entity_player as entity_player


class SystemEntityManager(system.System):
	def __init__(self):
		super(SystemEntityManager, self).__init__((component.LABEL_CONNECTION,))

	def update(self, dt, component_tuples):
		for game_pkg in self.world.get_entity(const.ENTITY_GAME_ID).components[component.LABEL_PACKAGE].packages:
			if game_pkg['pid'] == net.PID_JOIN:
				entity = entity_player.EntityPlayer(game_pkg['send_q'])
				entity.eid = game_pkg['eid']
				# TODO 临时
				component_control, component_transform = entity.components[component.LABEL_CONTROL], entity.components[component.LABEL_TRANSFORM]
				state = {'eid': entity.eid, 'fr': component_control.frame, 'p': component_transform.position.dict(), 'v': component_transform.velocity.dict()}
				entity.components[component.LABEL_CONNECTION].send_q.put({'pid': net.PID_ADD_MASTER, 'state': state})
				# entity.components[component.LABEL_CONNECTION].send_q.put({'pid': net.PID_ADD_MASTER, 'eid': entity.eid})
				# broadcast
				broadcast_pkg = {'pid': net.PID_ADD_REPLICA, 'state': state}
				# broadcast_pkg = {'pid': net.PID_ADD_REPLICA, 'eid': entity.eid}
				for _, component_tuple in component_tuples:
					component_connection, = component_tuple
					component_connection.send_q.put(broadcast_pkg)
				self.world.add_entity(entity)
				print('join:', entity.eid)
			elif game_pkg['pid'] == net.PID_DEL:
				entity = self.world.get_entity(game_pkg['eid'])
				entity.components[component.LABEL_CONNECTION].send_q.put(game_pkg)
				self.world.del_entity(entity)
				# broadcast
				broadcast_pkg = {'pid': net.PID_DEL_REPLICA, 'eid': entity.eid}
				for _, component_tuple in component_tuples:
					component_connection, = component_tuple
					component_connection.send_q.put(broadcast_pkg)
				print('del:', entity.eid)
