# coding=utf-8

entities = []


def add_entity(entity):
	entities.append(entity)


def get_entity(eid):
	for e in entities:
		if e.eid == eid:
			return e
	return None


def del_entity(eid):
	entities.remove(get_entity(eid))


def get_all_entities():
	return entities


def iter_entities(f):
	for e in entities:
		f(e)
