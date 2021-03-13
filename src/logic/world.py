# coding=utf-8

import pygame

import base.const as const
import base.clock as clock
import base.net as net
import base.ecs as ecs

import logic.system_reset as system_reset
import logic.system_package_dispatch as system_package_dispatch
import logic.system_entity_manager as system_entity_manager
import logic.system_recv_cmd as system_recv_cmd
import logic.system_physics as system_physics
import logic.system_control as system_control
import logic.system_recv_state as system_recv_state
import logic.system_sync_cmd as system_sync_cmd
import logic.system_game_event as system_game_event
import logic.system_render_logic as system_render_logic
import logic.system_rollback as system_rollback
import logic.system_interpolation as system_interpolation
import logic.system_dead_reckoning as system_dead_reckoning
import logic.system_render as system_render
import logic.system_sync_state as system_sync_state
import logic.entity_game as entity_game


class World(object):
	def __init__(self):
		self.systems = []
		self.entities = []
		if const.IS_CLIENT:
			pygame.init()
			pygame.display.set_caption('Physics Sync - Demo')
			# system
			self.add_system(system_reset.SystemReset())
			self.add_system(system_package_dispatch.SystemPackageDispatch())
			self.add_system(system_entity_manager.SystemEntityManager())
			self.add_system(system_recv_state.SystemRecvState())
			self.add_system(system_game_event.SystemGameEvent())
			self.add_system(system_control.SystemControl())
			self.add_system(system_sync_cmd.SystemSyncCmd())
			self.add_system(system_physics.SystemPhysics())
			self.add_system(system_rollback.SystemRollback())
			self.add_system(system_interpolation.SystemInterpolation())
			self.add_system(system_dead_reckoning.SystemDeadReckoning())
			self.add_system(system_render_logic.SystemRenderLogic())
			# render
			self.system_render = self.init_system(system_render.SystemRender())
			# join server
			net.send_client_pkg({'pid': net.PID_JOIN})
		else:
			# system
			self.add_system(system_package_dispatch.SystemPackageDispatch())
			self.add_system(system_entity_manager.SystemEntityManager())
			self.add_system(system_recv_cmd.SystemRecvCmd())
			self.add_system(system_physics.SystemPhysics())
			# state
			self.system_sync_state = self.init_system(system_sync_state.SystemSyncState())
		self.entities.append(entity_game.EntityGame())

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
		for sys in self.systems:
			sys.update(dt, self.component_tuples(sys))

	def update_roll_forward(self, dt):
		for sys in self.systems:
			if sys.roll_forward:
				sys.update(dt, self.component_tuples(sys))

	def update_render(self, dt):
		self.system_render.update(dt, self.component_tuples(self.system_render))

	def update_state(self, dt):
		self.system_sync_state.update(dt, self.component_tuples(self.system_sync_state))

	def component_tuples(self, system):
		comp_tuples = []
		for en in self.entities:
			comp_tuple = en.component_tuple(system.component_labels, system.component_label_mask)
			if comp_tuple is None:
				continue
			comp_tuples.append((en.eid, comp_tuple))
		return comp_tuples

	# ---------- entity ----------
	def add_entity(self, entity):
		self.entities.append(entity)

	def del_entity(self, entity):
		self.entities.remove(entity)

	def get_entity(self, eid):
		for en in self.entities:
			if en.eid == eid:
				return en
		return None

	# ---------- system ----------
	def add_system(self, system):
		self.systems.append(self.init_system(system))

	def init_system(self, system):
		system.init(self)
		return system

	# ---------- game single entity ----------
	def game_component(self, component_label):
		return self.get_entity(const.ENTITY_GAME_ID).get_component(component_label)

	def game_component_rollback(self, component_obj):
		self.get_entity(const.ENTITY_GAME_ID).add_component(component_obj)

	# ---------- master single entity ----------
	def master_eid(self):
		if const.IS_SERVER:
			return -1
		return self.game_component(ecs.LABEL_INFO).master_entity_id

	def master_component(self, component_label):
		if const.IS_SERVER:
			return None
		return self.get_entity(self.master_eid()).get_component(component_label)

	def master_component_rollback(self, component_obj):
		if const.IS_SERVER:
			return
		return self.get_entity(self.master_eid()).add_component(component_obj)
