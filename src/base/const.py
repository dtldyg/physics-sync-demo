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
GUI_MARGIN = (10, 10, 8, 2)
# GUI_SIZE = (84, 120, 24)  # when need show scroll-bar
GUI_SIZE = (90, 140, 24)

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

# EntityPhysics
ENTITY_RADIUS = 20
ENTITY_MASS = 1  # const
ENTITY_FRICTION = 400
ENTITY_FORCE = 1200
ENTITY_MAX_V = 800
ENTITY_RESTITUTION = 0.9

# EntityFlag (mask, val)
ENTITY_FLAG_MASTER = (1, 0)
ENTITY_FLAG_REPLICA = (1, 1)
ENTITY_FLAG_LOCAL = (1 << 1, 0)
ENTITY_FLAG_SHADOW = (1 << 1, 1)

# EntityInit
MASTER_CLIENT_COLOR = (255, 0, 0, 255)  # red
MASTER_SERVER_COLOR = (255, 0, 0, 127)  # red-half
REPLICA_CLIENT_COLOR = (0, 0, 255, 255)  # blue
REPLICA_SERVER_COLOR = (0, 0, 255, 127)  # blue-half

# --------- dynamic ---------

# FPS
RENDER_FPS = 120
LOGIC_FPS = 60  # 逻辑频率(cpu)，命令(上行带宽)
STATES_FPS = 10  # 状态(下行带宽)

# ControlMod
CONTROL_WASD = 'wasd'
CONTROL_MOUSE = '跟随鼠标'
CONTROL_LINE = '冲量'
CONTROL_MODE_LIST = [CONTROL_WASD, CONTROL_MOUSE, CONTROL_LINE]
CONTROL_MODE = CONTROL_WASD

# SyncMode
SHOW_SERVER = True
INPUT_BUFFER = True
MASTER_PREDICT = '预测'
MASTER_INTERPOLATION = '内插值'
MASTER_NONE = '无'
MASTER_BEHAVIOR_LIST = [MASTER_PREDICT, MASTER_INTERPOLATION, MASTER_NONE]
MASTER_BEHAVIOR = MASTER_PREDICT
REPLICA_INTERPOLATION = True
REPLICA_INTERPOLATION_LINEAR = '线性'
REPLICA_INTERPOLATION_CUBIC = '三次方'
REPLICA_INTERPOLATION_LIST = [REPLICA_INTERPOLATION_LINEAR, REPLICA_INTERPOLATION_CUBIC]
REPLICA_INTERPOLATION_MODE = REPLICA_INTERPOLATION_CUBIC
REPLICA_EXTRAPOLATION = True

# Network
NETWORK_CLIENT_BUFFER = 1  # only replica
NETWORK_SERVER_BUFFER = 6  # 60fps: 100ms delay
NETWORK_SERVER_BUFFER_MIN = 2

# Physics
PHYSICS_BLEND_FRAMES = 60
