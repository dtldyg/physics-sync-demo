# coding=utf-8

import pygame

_key_state = {}
_mouse_active = False


def refresh():
	global _mouse_active
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return False
		if event.type == pygame.KEYDOWN:
			_key_state[event.key] = True
		elif event.type == pygame.KEYUP:
			_key_state[event.key] = False
		elif event.type == pygame.WINDOWENTER:
			_mouse_active = True
		elif event.type == pygame.WINDOWLEAVE:
			_mouse_active = False
	return True


def key_state(key):
	if key in _key_state:
		return _key_state[key]
	return False


def mouse_active():
	return _mouse_active
