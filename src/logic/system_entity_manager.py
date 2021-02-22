# coding=utf-8

import base.net as net
import base.ecs as ecs
import base.math as math
import logic.entity_player as entity_player
import logic.entity_player_master as entity_player_master
import logic.entity_player_replica as entity_player_replica


class SystemEntityManager(ecs.System):
	def __init__(self):
		super(SystemEntityManager, self).__init__((ecs.LABEL_CONNECTION,))
		self.roll_forward = True

	def update(self, dt, component_tuples):
		for pkg in self.world.game_component(ecs.LABEL_PACKAGE).packages:
			if pkg['pid'] == net.PID_JOIN:
				entity = entity_player.EntityPlayer(pkg['eid'], pkg['send_q'])
				init_p = entity.get_component(ecs.LABEL_TRANSFORM).position.dict()
				entity.get_component(ecs.LABEL_CONNECTION).send_q.put({'pid': net.PID_ADD_MASTER, 'eid': entity.eid, 'p': init_p})
				# broadcast
				broadcast_pkg = {'pid': net.PID_ADD_REPLICA, 'eid': entity.eid, 'p': init_p}
				for _, comp_tuple in component_tuples:
					comp_connection, = comp_tuple
					comp_connection.send_q.put(broadcast_pkg)
				self.world.add_entity(entity)
				print('join:', entity.eid)
			elif pkg['pid'] == net.PID_DEL:
				entity = self.world.get_entity(pkg['eid'])
				entity.get_component(ecs.LABEL_CONNECTION).send_q.put(pkg)
				self.world.del_entity(entity)
				# broadcast
				broadcast_pkg = {'pid': net.PID_DEL_REPLICA, 'eid': entity.eid}
				for _, comp_tuple in component_tuples:
					comp_connection, = comp_tuple
					comp_connection.send_q.put(broadcast_pkg)
				print('del:', entity.eid)
			elif pkg['pid'] == net.PID_ADD_MASTER:
				init_p = math.Vector(**pkg['p'])
				entity = entity_player_master.EntityPlayerMaster(pkg['eid'], init_p)
				self.world.game_component(ecs.LABEL_INFO).master_entity_id = entity.eid
				self.world.add_entity(entity)
				print('add master:', entity.eid)
			elif pkg['pid'] == net.PID_ADD_REPLICA:
				init_p = math.Vector(**pkg['p'])
				entity = entity_player_replica.EntityPlayerReplica(pkg['eid'], init_p)
				self.world.add_entity(entity)
				print('add replica:', entity.eid)
			elif pkg['pid'] == net.PID_DEL_REPLICA:
				entity = self.world.get_entity(pkg['eid'])
				self.world.del_entity(entity)
				print('del replica:', entity.eid)
