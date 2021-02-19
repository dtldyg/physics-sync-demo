# coding=utf-8

import common.base.const as const
import common.net as net
import ecs.system as system
import ecs.component as component
import ecs.entity_player as entity_player
import ecs.entity_player_master as entity_player_master
import ecs.entity_player_replica as entity_player_replica


class SystemEntityManager(system.System):
	def __init__(self):
		super(SystemEntityManager, self).__init__((component.LABEL_CONNECTION,))

	def update(self, dt, component_tuples):
		for pkg in self.world.game_component(component.LABEL_PACKAGE).packages:
			if pkg['pid'] == net.PID_JOIN:
				entity = entity_player.EntityPlayer(pkg['eid'], pkg['send_q'])
				entity.components[component.LABEL_CONNECTION].send_q.put({'pid': net.PID_ADD_MASTER, 'eid': entity.eid})
				# broadcast
				broadcast_pkg = {'pid': net.PID_ADD_REPLICA, 'eid': entity.eid}
				for _, component_tuple in component_tuples:
					component_connection, = component_tuple
					component_connection.send_q.put(broadcast_pkg)
				self.world.add_entity(entity)
				print('join:', entity.eid)
			elif pkg['pid'] == net.PID_DEL:
				entity = self.world.get_entity(pkg['eid'])
				entity.components[component.LABEL_CONNECTION].send_q.put(pkg)
				self.world.del_entity(entity)
				# broadcast
				broadcast_pkg = {'pid': net.PID_DEL_REPLICA, 'eid': entity.eid}
				for _, component_tuple in component_tuples:
					component_connection, = component_tuple
					component_connection.send_q.put(broadcast_pkg)
				print('del:', entity.eid)
			elif pkg['pid'] == net.PID_ADD_MASTER:
				entity = entity_player_master.EntityPlayerMaster(pkg['eid'])
				self.world.add_entity(entity)
				print('add master:', entity.eid)
			elif pkg['pid'] == net.PID_ADD_REPLICA:
				entity = entity_player_replica.EntityPlayerReplica(pkg['eid'])
				self.world.add_entity(entity)
				print('add replica:', entity.eid)
			elif pkg['pid'] == net.PID_DEL_REPLICA:
				entity = self.world.get_entity(pkg['eid'])
				self.world.del_entity(entity)
				print('del replica:', entity.eid)
