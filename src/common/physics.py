# coding=utf-8

import common.base.const as const
import common.base.math as math


def pv_with_force_normal(p, v, f_nor, dt):
	if f_nor.zero() and v.zero():
		return p, v
	# --- 1.force analysis: Euler‘s Method ---
	# f = f - μ·mg·v_dir
	f_join = f_nor * const.ENTITY_FORCE - v.normal() * const.ENTITY_FRICTION * const.ENTITY_MASS * const.WORLD_G
	# a = f/m
	a = f_join / const.ENTITY_MASS
	# v = v0 + a·t
	v = v + a * dt
	if f_nor.zero() and v.length() <= a.length() * dt:
		# to zero
		v = math.vector_zero
	if v.length() > const.ENTITY_MAX_V:
		# to max
		v = v.normal() * const.ENTITY_MAX_V
	# s = v·t - similar to uniform motion
	s = v * dt
	# --- 2.v/p update ---
	p = p + s
	v = v
	return p, v


def pv_with_wall(p, v):
	# --- 3.collision check ---
	if p.x + const.ENTITY_RADIUS > const.SCREEN_SIZE[0]:
		v.x = -v.x
		p.x = const.SCREEN_SIZE[0] * 2 - const.ENTITY_RADIUS * 2 - p.x
	if p.y + const.ENTITY_RADIUS > const.SCREEN_SIZE[1]:
		v.y = -v.y
		p.y = const.SCREEN_SIZE[1] * 2 - const.ENTITY_RADIUS * 2 - p.y
	if p.x < const.ENTITY_RADIUS:
		v.x = -v.x
		p.x = const.ENTITY_RADIUS * 2 - p.x
	if p.y < const.ENTITY_RADIUS:
		v.y = -v.y
		p.y = const.ENTITY_RADIUS * 2 - p.y
	# --- 4.result show ---
	# TODO 碰撞时刻之后的作用力
	return p, v
