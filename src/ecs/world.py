# coding=utf-8

import common.base.const as const
import ecs.system_package_dispatch as system_package_dispatch
import ecs.system_entity_manager as system_entity_manager
import ecs.system_control as system_control
import ecs.system_physics as system_physics
import ecs.system_sync_state as system_sync_state
import ecs.entity_game as entity_game


class World(object):
	def __init__(self):
		self.entities = []
		self.systems = []
		if const.IS_CLIENT:
			self.rollback = False
		else:
			self.entities.append(entity_game.EntityGame())
			self.add_system(system_package_dispatch.SystemPackageDispatch())
			self.add_system(system_entity_manager.SystemEntityManager())
			self.add_system(system_control.SystemControl())
			self.add_system(system_physics.SystemPhysics())
			self.system_sync_state = system_sync_state.SystemSyncState()

	def update(self, dt):
		for system in self.systems:
			system.update(dt, self.component_tuples(system))

	def sync_state(self, dt):
		self.system_sync_state.update(dt, self.component_tuples(self.system_sync_state))

	def component_tuples(self, system):
		component_tuples = []
		for entity in self.entities:
			component_tuple = entity.component_tuple(system.component_labels, system.component_label_mask)
			if component_tuple is None:
				continue
			component_tuples.append((entity.eid, component_tuples))

	def add_entity(self, entity):
		self.entities.append(entity)

	def del_entity(self, entity):
		self.entities.remove(entity)

	def get_entity(self, eid):
		for entity in self.entities:
			if entity.eid == eid:
				return entity
		return None

	def add_system(self, system):
		system.init(self)
		self.systems.append(system)
