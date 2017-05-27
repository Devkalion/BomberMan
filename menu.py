from pygame import init, Color, Surface
from pygame.constants import *
from pygame.display import set_caption, set_icon, set_mode, update
from pygame.image import load
from pygame.event import get
from pygame.time import delay
from pygame.font import Font
from game import Play


class Menu:
    def __init__(self):
        init()
        set_caption('BomberMan')
        set_icon(load('Resources\images\icon.png'))
        self.screen = set_mode((1024, 768))
        self.load_images(Color('#115111'))
        self.btns = [(60, 522, 135, 572), (60, 575, 280, 625), (60, 627, 270, 677), (60, 678, 135, 728)]
        self.checked_btn = 0
        self.reload()
        self.cycle()

    def load_images(self, bg_color):
        self.logo = load('Resources\images\logo.png')
        self.bg = Surface((1024, 768))
        self.bg.fill(bg_color)
        self.menu = load('Resources\images\menu.bmp')
        self.menu.set_colorkey((81, 81, 81))
        self.man = load('Resources\images\man.png')
        self.submenu = Surface((50, 195))
        self.submenu.fill(bg_color)
        self.bomb = load('Resources\images\\bomb.png')
        self.explosion = load('Resources\images\Explosion.png')
        self.back = load('Resources\images\Back.bmp')
        self.back.set_colorkey((81, 81, 81))
        self.img1 = load('Resources\images\img1.png')

    def read_scores(self):
        f = open('Resources\Scores.txt', 'a+')
        f.seek(0)
        self.tabl = sorted([(s.split(' ')[0], int(s.split(' ')[1])) for s in f.readlines()], key=lambda x: -x[1])
        f.close()

    def reload(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.menu, (0, 520))
        self.screen.blit(self.logo, (30, 0))
        self.screen.blit(self.man, (540, 167))
        self.screen.blit(self.bomb, (20, self.btns[self.checked_btn][1] + 2))
        update()

    def cycle(self):
        n = 4  # Количество строк в меню
        while True:
            for event in get():
                if event.type == KEYDOWN:
                    k = event.key
                    if k == K_ESCAPE:
                        exit()
                    elif k == K_DOWN and self.checked_btn < n - 1:
                        self.checked_btn += 1
                        self.focus_changed(self.btns[self.checked_btn])
                    elif k == K_UP and self.checked_btn > 0:
                        self.checked_btn -= 1
                        self.focus_changed(self.btns[self.checked_btn])
                    elif k == 32 or k == 13 or k == 271:  # space, enter, small_enter
                        self.pressed(self.checked_btn, self.btns[self.checked_btn])
                elif event.type == QUIT:
                    exit()
                elif event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN and event.button == 1:
                    [x, y] = event.pos
                    for i in range(n):
                        if self.btns[i][0] <= x <= self.btns[i][2] and self.btns[i][1] <= y <= self.btns[i][3]:
                            if self.checked_btn != i:
                                self.checked_btn = i
                                self.focus_changed(self.btns[self.checked_btn])
                            if event.type == MOUSEBUTTONDOWN:
                                self.pressed(i, self.btns[i])
                            break

    def focus_changed(self, btn):
        self.screen.blit(self.submenu, (20, 524))
        self.screen.blit(self.bomb, (20, btn[1] + 2))
        update()

    def pressed(self, idx, btn):
        self.screen.blit(self.submenu, (20, 524))
        self.screen.blit(self.explosion, (20, btn[1] + 4))
        update()
        if idx != 3:
            delay(200)
        if idx == 0:
            Play(self.screen)
        elif idx == 1:
            self.instructions()
        elif idx == 2:
            if 'tabl' not in self.__dict__:
                self.read_scores()
            self.scores()
        else:
            exit()
        self.reload()

    def scores(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.logo, (30, 0))
        self.screen.blit(self.img1, (700, 300))
        self.screen.blit(self.back, (50, 690))
        font = Font('Resources\\font.ttf', 30)
        for i in range(len(self.tabl)):
            s = self.tabl[i]
            label = font.render(s[0], True, (255, 180, 0))
            self.screen.blit(label, (350, 240 + i * 50))
            label = font.render(str(s[1]), True, (255, 210, 0))
            self.screen.blit(label, (600, 240 + i * 50))
        update()
        ok = True
        while ok:
            for event in get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    ok = False
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    [x, y] = event.pos
                    if 30 <= x <= 146 and 700 <= y <= 746:
                        ok = False
                elif event.type == QUIT:
                    exit()

    def instructions(self):
        pass
