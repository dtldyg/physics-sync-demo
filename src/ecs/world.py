# coding=utf-8

import pygame

import common.base.const as const
import common.base.clock as clock

import ecs.component as component

import ecs.system_package_dispatch as system_package_dispatch
import ecs.system_entity_manager as system_entity_manager
import ecs.system_recv_cmd as system_recv_cmd
import ecs.system_physics as system_physics
import ecs.system_control as system_control
import ecs.system_recv_state as system_recv_state
import ecs.system_sync_cmd as system_sync_cmd
import ecs.system_game_event as system_game_event
import ecs.system_render_logic as system_render_logic
import ecs.system_rollback as system_rollback
import ecs.system_render as system_render
import ecs.system_sync_state as system_sync_state

import ecs.entity_game as entity_game


class World(object):
	def __init__(self):
		self.entities = [entity_game.EntityGame()]
		self.systems = []
		if const.IS_CLIENT:
			pygame.init()
			pygame.display.set_caption('Physics Sync - Demo')
			# system
			self.add_system(system_package_dispatch.SystemPackageDispatch())
			self.add_system(system_entity_manager.SystemEntityManager())
			self.add_system(system_recv_state.SystemRecvState())
			self.add_system(system_game_event.SystemGameEvent())
			self.add_system(system_control.SystemControl())
			self.add_system(system_sync_cmd.SystemSyncCmd())
			self.add_system(system_physics.SystemPhysics())
			self.add_system(system_render_logic.SystemRenderLogic())
			self.add_system(system_rollback.SystemRollback())
			# render
			self.system_render = system_render.SystemRender()
		else:
			# system
			self.add_system(system_package_dispatch.SystemPackageDispatch())
			self.add_system(system_entity_manager.SystemEntityManager())
			self.add_system(system_recv_cmd.SystemRecvCmd())
			self.add_system(system_physics.SystemPhysics())
			# state
			self.system_sync_state = system_sync_state.SystemSyncState()

	def run(self):
		c = clock.Clock()
		c.add(const.LOGIC_FPS, self.update)
		if const.IS_CLIENT:
			c.add(const.RENDER_FPS, self.update_render)
		else:
			c.add(const.STATES_FPS, self.update_state)
		print('world run')
		c.run()

	# ---------- update ----------
	def update(self, dt):
		for system in self.systems:
			system.update(dt, self.component_tuples(system))

	def update_render(self, dt):
		self.system_render.update(dt, self.component_tuples(self.system_render))

	def update_state(self, dt):
		self.system_sync_state.update(dt, self.component_tuples(self.system_sync_state))

	def component_tuples(self, system):
		component_tuples = []
		for entity in self.entities:
			component_tuple = entity.component_tuple(system.component_labels, system.component_label_mask)
			if component_tuple is None:
				continue
			component_tuples.append((entity.eid, component_tuple))
		return component_tuples

	# ---------- entity ----------
	def add_entity(self, entity):
		self.entities.append(entity)

	def del_entity(self, entity):
		self.entities.remove(entity)

	def get_entity(self, eid):
		for entity in self.entities:
			if entity.eid == eid:
				return entity
		return None

	# ---------- system ----------
	def add_system(self, system):
		system.init(self)
		self.systems.append(system)

	# ---------- game single entity ----------
	def game_component(self, component_label):
		return self.get_entity(const.ENTITY_GAME_ID).components[component_label]

	def game_component_rollback(self, component_label, component_obj):
		self.get_entity(const.ENTITY_GAME_ID).components[component_label] = component_obj

	# ---------- master single entity ----------
	def master_eid(self):
		return self.game_component(component.LABEL_GLOBAL).master_entity_id

	def master_component(self, component_label):
		return self.get_entity(self.master_eid()).components[component_label]
