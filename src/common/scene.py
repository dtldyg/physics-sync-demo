# coding=utf-8

entities = {}
entity_id = 0


def add_entity(entity):
	global entity_id
	entity.eid = entity_id
	entities[entity_id] = entity
	entity_id = entity_id + 1


def get_entity(eid):
	return entities[eid]


def del_entity(eid):
	del entities[eid]


def del_entities(eids):
	for eid in eids:
		del entities[eid]


def get_all_entities():
	return entities.values()


def iter_entities(f):
	for e in entities:
		f(e)
