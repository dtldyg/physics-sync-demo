# coding=utf-8

import copy
import ecs.system as system
import ecs.component as component


class SystemRollback(system.System):
	def __init__(self):
		super(SystemRollback, self).__init__((component.LABEL_PACKAGE, component.LABEL_PHYSICS, component.LABEL_TRANSFORM))

	def update(self, dt, component_tuples):
		# record
		component_record = self.world.game_component(component.LABEL_RECORD)
		component_package = self.world.game_component(component.LABEL_PACKAGE)
		component_frame = self.world.game_component(component.LABEL_FRAME)
		record = Record(dt, self.world.entities, component_package, component_frame)
		for eid, component_tuple in component_tuples:
			record.entities.append(RecordEntity(eid, *component_tuple))
		component_record.records.append(record)
		# rollback
		pass


class Record(object):
	def __init__(self, dt, entities, component_package, component_frame):
		self.dt = dt
		self.eids = [entity.eid for entity in entities]
		self.component_package = copy.deepcopy(component_package)
		self.component_frame = copy.deepcopy(component_frame)
		self.entities = []


class RecordEntity(object):
	def __init__(self, eid, component_package, component_physics, component_transform):
		self.eid = eid
		self.component_package = copy.deepcopy(component_package)
		self.component_physics = copy.deepcopy(component_physics)
		self.component_transform = copy.deepcopy(component_transform)
