from pygame.constants import *
from pygame.event import get
from pygame.mouse import set_visible
from pygame.key import set_repeat
from pygame.sprite import Group, collide_rect
from pygame.display import update
from pygame.image import load
from pygame.font import Font
from pygame.time import get_ticks, wait
from pygame import Surface, Color
from Mobs import Sprites, Mobs, Player
from random import randint


class Play:
    def __init__(self, screen, color):
        self.screen = screen
        self.bg = Surface((1024, 718))
        self.bg.fill(color)
        self.info = Surface((1024, 50))
        self.info.fill(color)
        self.ground = load('Resources\images\Sprites\Tiles\\0.png')
        self.bomb_info = load('Resources\images\\bomb.png')
        self.life_info = load('Resources\images\life.png')
        self.power_info = load('Resources\images\power.png')
        self.lvl = 1
        self.lives = 3
        self.max_bombs = 3
        self.strength = 1
        set_visible(False)
        self.load_level()
        self.play()
        set_visible(True)
        set_repeat()

    def load_level(self):
        self.begin = [0, 0]
        self.mobs = Group()
        self.sprites = Group()
        self.grass = Group()
        self.blocks = Group()
        try:
            f = open('Resources\level' + str(self.lvl) + '.txt', 'r')
        except:
            self.win()
            return
        self.board = [s[0:(len(s) - 1)] for s in f.readlines()]
        n = len(self.board)
        m = len(self.board[0])
        for i in range(n):
            for j in range(m):
                if self.board[i][j] == '1':
                    s = Sprites(self.screen, 'Tiles\\3.png', j * 40 + 5, i * 40 + 55, self.begin, False)
                    s.image = load('Resources\images\Sprites\Tiles\\1.png')
                    s.rect.x -= 5
                    s.rect.y -= 5
                    self.sprites.add(s)
                else:
                    self.grass.add(Sprites(self.screen, 'Tiles\\0.png', j * 40, i * 40 + 50, self.begin))
                    if self.board[i][j] == '2':
                        s = Sprites(self.screen, 'Tiles\\3.png', j * 40 + 5, i * 40 + 55, self.begin)
                        s.image = load('Resources\images\Sprites\Tiles\\2.png')
                        s.rect.x -= 5
                        s.rect.y -= 5
                        self.sprites.add(s)
                        self.blocks.add(s)
                    elif self.board[i][j] == 'P':
                        self.start_pos = (j * 40, i * 40 + 50)
                        self.hero = Player(self.screen, j * 40, i * 40 + 50, self.max_bombs
                                           , self.strength, self.begin, m * 40, n * 40)
                    elif self.board[i][j] != '0':
                        self.mobs.add(Mobs(self.screen, self.board[i][j], j * 40, i * 40 + 50, 0.9, randint(0, 3), self.begin))
        f.close()
        self.start = get_ticks()

    def play(self):
        self.time = get_ticks()
        self.ok = True
        set_repeat(10, 10)
        while self.ok:
            for event in get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    k = event.key
                    if k == K_ESCAPE:
                        self.ok = False
                    if k == K_DOWN:
                        self.hero.rotate(0)
                        self.hero.ismoved = True
                    if k == K_UP:
                        self.hero.rotate(1)
                        self.hero.ismoved = True
                    if k == K_RIGHT:
                        self.hero.rotate(2)
                        self.hero.ismoved = True
                    if k == K_LEFT:
                        self.hero.rotate(3)
                        self.hero.ismoved = True
                    if k == K_SPACE:
                        self.hero.place_bomb()
                elif event.type == KEYUP and event.key != 32:
                    self.hero.ismoved = False
            for m in self.mobs:
                m.strategy()
            self.time = max(get_ticks(), self.time)
            self.screen.blit(self.bg, (0, 50))
            self.grass.update()
            self.sprites.update()
            self.hero.update(self.sprites)
            self.hero.explosions.update()
            tmp = self.sprites.copy()
            for b in self.hero.bombs:
                tmp.add(b)
            self.mobs.update(tmp)
            self.show_info()
            update()
            for ex in self.hero.explosions:
                if self.time + 700 < ex.clear_time:
                    for b in self.hero.bombs:
                        if collide_rect(b, ex):
                            b.explosion_time = 0
                    for m in self.mobs:
                        if collide_rect(m, ex):
                            m.kill()
                    for b in self.blocks:
                        if collide_rect(b, ex):
                            b.kill()
            for ex in self.hero.explosions:
                if self.time + 700 < ex.clear_time and collide_rect(self.hero, ex):
                    self.death()
                    break
            if self.hero.collide(self.mobs):
                self.death()
            if len(self.mobs) == 0:
                self.lvl += 1
                self.load_level()

    def death(self):
        self.lives -= 1
        if self.lives < 0:
            self.lose()
            return
        self.begin[0] = 0
        self.begin[1] = 0
        self.max_bombs = 1
        self.strength = 1
        self.hero = Player(self.screen, self.start_pos[0], self.start_pos[1], self.max_bombs,
                           self.strength, self.begin, len(self.board[0]) * 40, len(self.board) * 40)
        wait(700)
        while self.hero.collide(self.mobs):
            wait(500)

    def lose(self):
        self.ok = False

    def win(self):
        self.ok = False

    def update_timer(self):
        s = 60 - (get_ticks() - self.start) // 1000
        if s == 0:
            self.lose()
            return
        self.screen.blit(self.info, (700, 0))
        font = Font('Resources\\font.ttf', 30)
        s1 = ''
        if s % 60 < 10:
            s1 = '0'
        label = font.render('Time ' + str(s // 60) + ':' + s1 + str(s % 60), True, (255, 180, 0))
        self.screen.blit(label, (850, 5))

    def show_info(self):
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
        self.update_timer()
