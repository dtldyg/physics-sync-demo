# coding=utf-8
import sys
import time
import pygame
import pygame.color

# Game
FPS = 60
FPS_COLOR = (255, 255, 0, 255)  # yellow
SCREEN_SIZE = (800, 400)
SCREEN_BACKGROUND = (0, 0, 0, 255)  # black
# World
WORLD_G = 1  # const
WORLD_F = 4  # ctrl force
# Entity
ENTITY_RADIUS = 20  # radius
ENTITY_MASS = 1  # const
ENTITY_FRICTION = 1  # friction μ
MASTER_INIT_POS = (50, SCREEN_SIZE[1] / 2)
MASTER_COLOR = (255, 0, 0, 255)  # red
REPLICA_INIT_POS = (SCREEN_SIZE[0] - MASTER_INIT_POS[0], SCREEN_SIZE[1] / 2)
REPLICA_COLOR = (255, 255, 255, 255)  # white


class Vector(object):
	def __init__(self, x=0, y=0):
		self.x, self.y = x, y

	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y)

	def __mul__(self, other):
		return Vector(self.x * other, self.y * other)

	def __truediv__(self, other):
		return Vector(self.x / other, self.y / other)

	def tuple(self):
		return self.x, self.y

	def length(self):
		return (self.x ** 2 + self.y ** 2) ** 0.5

	def zero(self):
		return self.x == 0 and self.y == 0

	def normal(self):
		length = self.length()
		if length > 0:
			return Vector(self.x / length, self.y / length)
		else:
			return Vector()


class MasterEntity(object):
	def __init__(self, screen):
		self.screen = screen
		self.lt = time.time()
		self.pos = Vector(*MASTER_INIT_POS)
		self.velocity = Vector()

	def update(self, ctrl):
		now = time.time()
		self.lt, dt = now, now - self.lt
		ctrl.normal()
		self._update_physics(ctrl, dt)
		pygame.draw.circle(self.screen, MASTER_COLOR, self.pos.tuple(), ENTITY_RADIUS)

	def _update_physics(self, ctrl, dt):
		if ctrl.zero() and self.velocity.zero():
			return
		# f = f·dir - μ·mg·dir
		f = ctrl * WORLD_F - self.velocity.normal() * ENTITY_FRICTION * ENTITY_MASS * WORLD_G
		# a = f/m
		a = f / ENTITY_MASS
		# v = v0 + at
		v = self.velocity + a * dt
		# s = v0t + 1/2at2
		s = self.velocity + a * 0.5 * (dt ** 2)
		self.velocity = v
		self.pos = self.pos + s


def get_fps(t):
	if t <= 0:
		return 1
	return int(1 / t * 1000)


key_state = {
	pygame.K_w: False,
	pygame.K_s: False,
	pygame.K_a: False,
	pygame.K_d: False,
}


def get_input_vec():
	x, y = 0, 0
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			key_state[event.key] = True
		elif event.type == pygame.KEYUP:
			key_state[event.key] = False
	if key_state[pygame.K_w]:
		y = -1
	if key_state[pygame.K_s]:
		y = 1
	if key_state[pygame.K_a]:
		x = -1
	if key_state[pygame.K_d]:
		x = 1
	return Vector(x, y)


def main():
	pygame.init()
	pygame.display.set_caption('Physics Sync - Demo')

	clock = pygame.time.Clock()
	font = pygame.font.SysFont('arial', 16)

	screen = pygame.display.set_mode(SCREEN_SIZE)
	screen.fill(SCREEN_BACKGROUND)

	master_entity = MasterEntity(screen)

	fps = 0

	while True:
		# input
		input_vec = get_input_vec()
		# clean scene
		screen.fill(SCREEN_BACKGROUND)

		# update all entity
		master_entity.update(input_vec)

		# calc fps
		fps_text = font.render('fps:{}'.format(fps), True, FPS_COLOR)
		screen.blit(fps_text, (0, 0))
		# re-draw the scene
		pygame.display.flip()
		# fps limit
		fps = get_fps(clock.tick(FPS))


if __name__ == "__main__":
	main()
