# coding=utf-8

import sys
import pygame

_key_state = {}


def refresh():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			_key_state[event.key] = True
		elif event.type == pygame.KEYUP:
			_key_state[event.key] = False


def key_state(key):
	if key in _key_state:
		return _key_state[key]
	return False
