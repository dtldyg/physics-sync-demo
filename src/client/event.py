# coding=utf-8

import pygame

_key_state = {}
_mouse_state = {'active': False, 'trigger': {'down': {}, 'up': {}}}


def refresh(panel_gui):
	_mouse_state['trigger']['down'].clear()
	_mouse_state['trigger']['up'].clear()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return False
		if event.type == pygame.KEYDOWN:
			_key_state[event.key] = True
		elif event.type == pygame.KEYUP:
			_key_state[event.key] = False
		elif event.type == pygame.WINDOWENTER:
			_mouse_state['active'] = True
		elif event.type == pygame.WINDOWLEAVE:
			_mouse_state['active'] = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			_mouse_state['trigger']['down'][event.button] = None
		elif event.type == pygame.MOUSEBUTTONUP:
			_mouse_state['trigger']['up'][event.button] = None
		panel_gui.process_events(event)
	return True


def key_state(key):
	if key in _key_state:
		return _key_state[key]
	return False


def mouse_active():
	return _mouse_state['active']


def mouse_trigger_down(btn):
	return btn in _mouse_state['trigger']['down']


def mouse_trigger_up(btn):
	return btn in _mouse_state['trigger']['up']
