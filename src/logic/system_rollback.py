# coding=utf-8

import copy
import base.const as const
import base.ecs as ecs


class SystemRollback(ecs.System):
	def __init__(self):
		super(SystemRollback, self).__init__((ecs.LABEL_PHYSICS, ecs.LABEL_TRANSFORM))

	def update(self, dt, component_tuples):
		comp_record = self.world.game_component(ecs.LABEL_RECORD)
		if not const.MASTER_PREDICT:
			comp_record.clear()
			return
		# record
		comp_package = self.world.game_component(ecs.LABEL_PACKAGE)
		comp_frame = self.world.master_component(ecs.LABEL_FRAME)
		record = Record(dt, self.world.entities, comp_package, comp_frame)
		for eid, comp_tuple in component_tuples:
			record.entities[eid] = RecordEntity(eid, *comp_tuple)
		comp_record.records.append(record)
		# rollback
		while comp_record.server_frame > comp_record.records[0].component_frame.frame:
			comp_record.records.pop(0)
		comp_transform = self.world.master_component(ecs.LABEL_TRANSFORM)
		record_transform = None
		for record_entity in comp_record.records[0].entities:
			if record_entity.eid == self.world.master_eid():
				record_transform = record_entity.component_transform
				break
		if not transform_near(comp_transform, record_transform):
			for record in comp_record.records:
				if record == comp_record.records[0]:
					# roll-back record
					record_transform.position = comp_transform.server_position
					record_transform.velocity = comp_transform.server_velocity
					# roll-back world
					self.world.entities = [en for en in self.world.entities if en.eid in record.eids]
					for en in self.world.entities:
						record_entity = record.entities[en.eid]
						en.add_component(record_entity.component_transform)
				else:
					# roll-forward world
					self.world.game_component_rollback(copy.deepcopy(record.component_package))
					for en in self.world.entities:
						record_entity = record.entities[en.eid]
						en.add_component(copy.deepcopy(record_entity.component_physics))
					self.world.update_roll_forward(record.dt)
					# roll-forward record
					for en in self.world.entities:
						record_entity = record.entities[en.eid]
						record_entity.component_transform = copy.deepcopy(en.get_component(component.LABEL_TRANSFORM))


def transform_near(server_trans, record_trans):
	return server_trans.server_position.near(record_trans.position) and server_trans.server_velocity.near(record_trans.velocity)


class Record(object):
	def __init__(self, dt, entities, component_package, component_frame):
		self.dt = dt
		self.eids = set([en.eid for en in entities])
		self.component_package = copy.deepcopy(component_package)
		self.component_frame = copy.deepcopy(component_frame)
		self.entities = {}


class RecordEntity(object):
	def __init__(self, component_package, component_physics, component_transform):
		self.component_physics = copy.deepcopy(component_physics)
		self.component_transform = copy.deepcopy(component_transform)