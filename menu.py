import pygame
from pygame import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
bg = Surface((800, 600))
bg.fill(Color('#004400'))
pygame.display.set_caption('BomberMan')
checked_btn = 1
n = 5  # Количество строк в меню
objects = []

opened = True
while opened:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            k = event.key
            if k == K_ESCAPE:
                opened = False
            elif k == K_DOWN:
                checked_btn = min(checked_btn + 1, n)
            elif k == K_UP:
                checked_btn = max(checked_btn - 1, 1)
        elif event.type == QUIT:
            opened = False
    screen.blit(bg, (0, 0))
    pygame.display.update()

