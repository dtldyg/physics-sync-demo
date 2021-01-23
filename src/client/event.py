# coding=utf-8

import pygame

_key_state = {}


def refresh():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return False
		if event.type == pygame.KEYDOWN:
			_key_state[event.key] = True
		elif event.type == pygame.KEYUP:
			_key_state[event.key] = False
	return True


def key_state(key):
	if key in _key_state:
		return _key_state[key]
	return False
