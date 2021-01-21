# coding=utf-8

# Game
FPS = 60
FPS_COLOR = (0, 255, 0, 255)  # green
SCREEN_SIZE = (400, 400)
SCREEN_BACKGROUND = (0, 0, 0, 255)  # black
# World
WORLD_G = 1  # const
# Entity
ENTITY_RADIUS = 20  # radius
ENTITY_MASS = 1  # const
ENTITY_FRICTION = 1  # friction μ
ENTITY_FORCE = 4  # ctrl force

MASTER_INIT_POS = (50, SCREEN_SIZE[1] / 2)
MASTER_COLOR = (255, 0, 0, 255)  # red
REPLICA_INIT_POS = (SCREEN_SIZE[0] - MASTER_INIT_POS[0], SCREEN_SIZE[1] / 2)
REPLICA_COLOR = (255, 255, 0, 255)  # yellow
