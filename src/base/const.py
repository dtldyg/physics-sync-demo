# coding=utf-8

# --------- static ---------

# Env
IS_CLIENT = False
IS_SERVER = False

# Screen
FPS_COLOR = (0, 255, 0, 255)  # green
SCREEN_SIZE = (400, 400)
SCREEN_BACKGROUND = (0, 0, 0, 255)  # black

# GUI
GUI_WIDTH = 260
GUI_BACKGROUND = (30, 30, 30, 255)  # gray
GUI_MARGIN = (10, 10, 12, 2)
GUI_SIZE = (100, 140, 26)

# Game
PING_FPS = 2
CONTROL_LINE_COLOR = (255, 255, 255, 255)  # white
CONTROL_LINE_WIDTH = 1
CONTROL_LINE_RADIUS = int(SCREEN_SIZE[1] / 2)
CONTROL_LINE_TIME = 1

# ECS
ENTITY_GAME_ID = 0

# World
WORLD_G = 1  # const

# Physics
COLLISION_ITERATION = 5

# Entity
ENTITY_RADIUS = 20
ENTITY_MASS = 1  # const
ENTITY_FRICTION = 400
ENTITY_FORCE = 1200
ENTITY_MAX_V = 800

# EntityFlag (mask, val)
ENTITY_FLAG_MASTER = (1, 0)
ENTITY_FLAG_REPLICA = (1, 1)
ENTITY_FLAG_LOCAL = (1 << 1, 0)
ENTITY_FLAG_SHADOW = (1 << 1, 1)

# EntityInit
MASTER_INIT_POS = (50, SCREEN_SIZE[1] / 2)
MASTER_CLIENT_COLOR = (255, 0, 0, 255)  # red
MASTER_SERVER_COLOR = (255, 0, 0, 127)  # red-half
REPLICA_COLOR = (255, 255, 0, 255)  # yellow
REPLICA_SHADOW_COLOR = (255, 255, 0, 127)  # yellow-half

# --------- dynamic ---------

# FPS
RENDER_FPS = 120
LOGIC_FPS = 30  # 逻辑频率(cpu)，命令(上行带宽)
STATES_FPS = 10  # 状态(下行带宽)

# ControlMod
CONTROL_WASD = 'WASD'
CONTROL_MOUSE = 'M_Follow'
CONTROL_LINE = 'M_Line'
CONTROL_MODE_LIST = [CONTROL_WASD, CONTROL_MOUSE, CONTROL_LINE]
CONTROL_MODE = CONTROL_WASD

# SyncMode
MASTER_PREDICT = True
MASTER_SERVER = True
REPLICA_BUFFER = False
REPLICA_INTERPOLATION = False
REPLICA_EXTRAPOLATION = False

# Network
NETWORK_CLIENT_BUFFER = 0
NETWORK_SERVER_BUFFER = 0

# Physics
PHYSICS_BLEND_FRAMES = 60