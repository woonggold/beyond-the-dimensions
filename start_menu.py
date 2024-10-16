import pygame
from pygame.locals import *

screen = pygame.display.set_mode((1200, 800))
running = True

while (running == True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    pygame.display.update()