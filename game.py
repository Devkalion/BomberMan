from pygame.constants import *
from pygame.event import get
from pygame.mouse import set_visible
from pygame.key import set_repeat
from pygame.sprite import Group
from pygame.display import update
from pygame.image import load
from pygame.font import Font
from pygame.time import get_ticks
from pygame import Surface, Color
from Mobs import Sprites, Mobs, Player
from random import randint

class Play:
    def __init__(self, screen):
        self.screen = screen
        self.load_images()
        self.lvl = 1
        self.lives = 3
        self.max_bombs = 1
        self.strength = 1
        self.change_info()
        self.load_level(self.lvl)
        set_visible(False)
        self.start = get_ticks()
        self.play()
        set_visible(True)
        set_repeat()

    def load_images(self):
        self.bg = Surface((1024, 718))
        self.bg.fill(Color('#515151'))
        self.info = Surface((1024, 50))
        self.info.fill(Color('#515151'))
        self.ground = load('Resources\images\Sprites\Tiles\\0.png')
        self.bomb_info = load('Resources\images\\bomb.png')
        self.life_info = load('Resources\images\life.png')
        self.power_info = load('Resources\images\power.png')

    def load_level(self, num):
        self.mobs = Group()
        self.sprites = Group()
        self.grass = Group()
        f = open('Resources\level' + str(num) + '.txt', 'r')
        self.board = [s[0:(len(s) - 1)] for s in f.readlines()]
        n = len(self.board)
        m = len(self.board[0])
        for i in range(n):
            for j in range(m):
                if self.board[i][j] == '1':
                    s = Sprites(self.screen, 'Tiles\\3.png', j * 40 + 5, i * 40 + 55)
                    s.image = load('Resources\images\Sprites\Tiles\\1.png')
                    s.rect.x -= 5
                    s.rect.y -= 5
                    self.sprites.add(s)
                elif self.board[i][j] == '2':
                    self.sprites.add(Sprites(self.screen, 'Tiles\\2.png', j * 40, i * 40 + 50))
                else:
                    if self.board[i][j] == 'P':
                        self.hero = Player(self.screen, j * 40, i * 40 + 50, self.max_bombs, self.strength)
                    elif self.board[i][j] != '0':
                        self.mobs.add(Mobs(self.screen, self.board[i][j], j * 40, i * 40 + 50, 0.7, randint(0, 3)))
                    self.grass.add(Sprites(self.screen, 'Tiles\\0.png', j * 40, i * 40 + 50))
        f.close()

    def play(self):
        ok = True
        set_repeat(1, 1)
        while ok:
            for event in get():
                ismoved = False
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    k = event.key
                    if k == K_ESCAPE:
                        ok = False
                    if k == K_DOWN:
                        self.hero.rotate(0)
                        ismoved = True
                    if k == K_UP:
                        self.hero.rotate(1)
                        ismoved = True
                    if k == K_RIGHT:
                        self.hero.rotate(2)
                        ismoved = True
                    if k == K_LEFT:
                        self.hero.rotate(3)
                        ismoved = True
                    if k == K_SPACE:
                        self.hero.place_bomb()
            for m in self.mobs:
                m.strategy()
            self.screen.blit(self.bg, (0, 50))
            self.grass.update()
            self.sprites.update()
            self.hero.update(self.sprites, ismoved)
            self.mobs.update(self.sprites)
            self.update_timer()
            update()

    def update_timer(self):
        s = 180 - (get_ticks() - self.start) // 1000
        self.screen.blit(self.info, (700, 0))
        font = Font('Resources\\font.ttf', 30)
        s1 = ''
        if s % 60 < 10:
            s1 = '0'
        label = font.render('Time ' + str(s // 60) + ':' + s1 + str(s % 60), True, (255, 180, 0))
        self.screen.blit(label, (850, 5))

    def change_info(self):
        self.screen.blit(self.info, (0, 0))
        font = Font('Resources\\font.ttf', 30)
        label = font.render('level ' + str(self.lvl), True, (255, 180, 0))
        self.screen.blit(label, (40, 5))

        self.screen.blit(self.life_info, (240, 5))
        label = font.render(str(self.lives), True, (255, 180, 0))
        self.screen.blit(label, (290, 5))

        self.screen.blit(self.bomb_info, (350, 5))
        label = font.render(str(self.max_bombs), True, (255, 180, 0))
        self.screen.blit(label, (400, 5))

        self.screen.blit(self.power_info, (455, 5))
        label = font.render(str(self.strength), True, (255, 180, 0))
        self.screen.blit(label, (500, 5))
