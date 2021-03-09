# coding=utf-8

import itertools
import base.net as net
import base.ecs as ecs
import base.math as math
import base.const as const
import logic.entity_player as entity_player
import logic.entity_player_master as entity_player_master
import logic.entity_player_replica as entity_player_replica


class SystemEntityManager(ecs.System):
	def __init__(self):
		super(SystemEntityManager, self).__init__((ecs.LABEL_CONNECTION, ecs.LABEL_TRANSFORM))
		self.roll_forward = True

	def update(self, dt, component_tuples):
		entity_grid = None
		for pkg in self.world.game_component(ecs.LABEL_PACKAGE).packages:
			if pkg['pid'] == net.PID_JOIN:
				entity_grid = entity_grid or {}
				for eid, comp_tuple in component_tuples:
					_, comp_transform = comp_tuple
					add_grid(entity_grid, comp_transform.position)
				entity = entity_player.EntityPlayer(pkg['eid'], choose_grid_to_pos(entity_grid), pkg['send_q'])
				init_p = entity.get_component(ecs.LABEL_TRANSFORM).position.dict()
				comp_connection = entity.get_component(ecs.LABEL_CONNECTION)
				comp_connection.send_q.put({'pid': net.PID_ADD_MASTER, 'eid': entity.eid, 'p': init_p})
				for eid, comp_tuple in component_tuples:
					_, comp_transform = comp_tuple
					print(eid)
					comp_connection.send_q.put({'pid': net.PID_ADD_REPLICA, 'eid': eid, 'p': comp_transform.position.dict()})
				# broadcast
				broadcast_pkg = {'pid': net.PID_ADD_REPLICA, 'eid': entity.eid, 'p': init_p}
				for _, comp_tuple in component_tuples:
					comp_connection, _ = comp_tuple
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
					comp_connection, _ = comp_tuple
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


def add_grid(entity_grid, position):
	grid_len = const.ENTITY_RADIUS * 2
	x_idx = int(position.x / grid_len)
	y_idx = int(position.y / grid_len)
	x_over = position.x % grid_len
	y_over = position.y % grid_len
	x_offset, y_offset = 0, 0
	if x_over != const.ENTITY_RADIUS:
		x_offset = 1 if x_over > const.ENTITY_RADIUS else -1
	if y_over != const.ENTITY_RADIUS:
		y_offset = 1 if y_over > const.ENTITY_RADIUS else -1
	for grid_idx in itertools.product([x_idx, x_idx + x_offset], [y_idx, y_idx + y_offset]):
		if grid_idx[0] not in entity_grid:
			entity_grid[grid_idx[0]] = {}
		entity_grid[grid_idx[0]][grid_idx[1]] = True


def choose_grid_to_pos(entity_grid):
	grid_len = const.ENTITY_RADIUS * 2
	x_num = int(const.SCREEN_SIZE[0] / grid_len)
	y_num = int(const.SCREEN_SIZE[1] / grid_len)
	for x in range(1, x_num - 1):
		for y in range(1, y_num - 1):
			if x not in entity_grid or y not in entity_grid[x]:
				return [x * grid_len + const.ENTITY_RADIUS, y * grid_len + const.ENTITY_RADIUS]
	return [const.ENTITY_RADIUS, const.ENTITY_RADIUS]
