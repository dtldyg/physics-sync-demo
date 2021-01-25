# coding=utf-8

entities = []


def add_entity(entity):
	entities.append(entity)


def iter_entities(f):
	for e in entities:
		f(e)
