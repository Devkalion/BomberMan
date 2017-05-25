import pygame
from pygame import *
from game import Play

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768))
        self.bg = pygame.image.load('Resources\images\menu.png').convert()
        pygame.display.set_caption('BomberMan')
        self.screen.blit(self.bg, (0, 0))
        self.cycle()

    def cycle(self):
        n = 4  # Количество строк в меню
        checked_btn = 0
        btns = [(60, 522, 120, 572), (60, 575, 260, 625), (60, 627, 250, 677), (60, 675, 120, 725)]
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    k = event.key
                    if k == K_ESCAPE:
                        exit()
                    elif k == K_DOWN and checked_btn < n - 1:
                        checked_btn += 1
                    elif k == K_UP and checked_btn > 0:
                        checked_btn -= 1
                    elif k == 32 or k == 271 or k == 13:  # space, enter, small_enter
                        self.pressed(checked_btn)
                elif event.type == QUIT:
                    exit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    [x, y] = event.pos
                    for i in range(n):
                        if btns[i][0] <= x <= btns[i][2] and btns[i][1] <= y <= btns[i][3]:
                            self.pressed(i)
                            break
            self.screen.blit(pygame.image.load('Resources\images\submenu.bmp').convert(), (0, 502))
            self.screen.blit(pygame.image.load('Resources\images\\bomb.png').convert(), (20, btns[checked_btn][1]))
            pygame.display.update()

    def pressed(self, idx):
        if idx == 0:
            Play(self.screen)
        elif idx == 1:
            self.instructions()
        elif idx == 2:
            self.scores()
        else:
            exit()

    def scores(self):
        pass

    def instructions(self):
        pass

