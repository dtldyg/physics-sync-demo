# coding=utf-8

import copy
import base.const as const
import base.ecs as ecs


class SystemRollback(ecs.System):
	def __init__(self):
		super(SystemRollback, self).__init__((ecs.LABEL_PHYSICS, ecs.LABEL_TRANSFORM, ecs.LABEL_INTERPOLATION))

	def update(self, dt, component_tuples):
		master_eid = self.world.master_eid()
		if master_eid == 0:
			return
		game_comp_record = self.world.game_component(ecs.LABEL_RECORD)
		records = game_comp_record.records
		if const.MASTER_BEHAVIOR != const.MASTER_PREDICT:
			records.clear()
			return
		game_comp_package = self.world.game_component(ecs.LABEL_PACKAGE)
		master_comp_frame = self.world.master_component(ecs.LABEL_FRAME)
		master_comp_transform = self.world.master_component(ecs.LABEL_TRANSFORM)

		# record
		record = Record(dt, self.world.entities, game_comp_package, master_comp_frame, component_tuples)
		records.append(record)

		# rollback
		if not master_comp_transform.server_modified:
			return
		while master_comp_frame.server_frame > records[0].component_frame.frame:
			records.pop(0)  # pop confirmed record
		record_transform = records[0].entities[master_eid].components[ecs.LABEL_TRANSFORM]
		if not transform_near(master_comp_transform, record_transform):
			game_comp_record.rollback = True
			game_comp_record.rollback_notify = True
			for record in records:
				if record == records[0]:
					# roll-back record
					record_transform.position = master_comp_transform.server_position
					record_transform.velocity = master_comp_transform.server_velocity
					# roll-back world
					self.world.entities = [en for en in self.world.entities if en.eid in record.eids]
					for en in self.world.entities:
						if en.eid == const.ENTITY_GAME_ID:
							continue
						for record_component in record.entities[en.eid].components.values():
							en.add_component(record_component)
				else:
					# roll-forward world
					self.world.game_component_rollback(copy.deepcopy(record.component_package))
					self.world.master_component_rollback(copy.deepcopy(record.entities[master_eid].components[ecs.LABEL_PHYSICS]))  # set force
					self.world.update_roll_forward(record.dt)
					# roll-forward record
					for en in self.world.entities:
						if en.eid == const.ENTITY_GAME_ID:
							continue
						comp_tuple = en.component_tuple(self.component_labels, self.component_label_mask)
						record.entities[en.eid] = RecordEntity(comp_tuple)
			game_comp_record.rollback = False


def transform_near(server_trans, record_trans):
	return server_trans.server_position.near(record_trans.position) and server_trans.server_velocity.near(record_trans.velocity)


class Record(object):
	def __init__(self, dt, entities, component_package, component_frame, component_tuples):
		self.dt = dt
		self.eids = set([en.eid for en in entities])
		self.component_package = copy.deepcopy(component_package)
		self.component_frame = copy.deepcopy(component_frame)
		self.entities = {}
		for eid, comp_tuple in component_tuples:
			self.entities[eid] = RecordEntity(comp_tuple)


class RecordEntity(object):
	def __init__(self, comp_tuple):
		self.components = {}
		for component in comp_tuple:
			self.components[component.label] = copy.deepcopy(component)
