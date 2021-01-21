# coding=utf-8

import time
import pygame

pygame.init()
screen = pygame.display.set_mode((200, 200))
clock = pygame.time.Clock()

screen.fill((255, 0, 0, 255))
time.sleep(3)
pygame.display.flip()
