from pygame.constants import QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_DOWN, K_RIGHT, K_LEFT, K_UP, K_SPACE
from pygame.event import get
from pygame.mouse import set_visible
from pygame.key import set_repeat
from pygame.sprite import Group, collide_rect, spritecollideany
from pygame.display import update
from pygame.image import load
from pygame.font import Font
from pygame.time import get_ticks, wait
from pygame import Surface
from Mobs import Sprites, Mobs, Player, Bonus
from random import randint


class Play:
    def __init__(self, screen, color):
        self.end = False
        self.screen = screen
        self.color = color
        self.info = Surface((1024, 50))
        self.info.fill(color)
        self.ground = load('Resources\images\Sprites\Tiles\\0.png')
        self.bomb_info = load('Resources\images\\bomb.png')
        self.life_info = load('Resources\images\life.png')
        self.power_info = load('Resources\images\power.png')
        self.lvl = 1
        self.scores = 0
        self.lives = 3
        self.max_bombs = 1
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
        self.sprites_and_bombs = Group()
        self.grass = Group()
        self.bonuses = Group()
        try:
            f = open('Resources\level' + str(self.lvl) + '.txt', 'r')
        except:
            self.win()
            return
        self.screen.blit(load('Resources\images\loading.jpg'), (0, 0))
        update()
        wait(1000)
        self.board = [s[0:(len(s) - 1)] for s in f.readlines()]
        n = len(self.board)
        m = len(self.board[0])
        for i in range(n):
            for j in range(m):
                (x, y) = j * 40, i * 40 + 50
                if self.board[i][j] == '1':
                    s = Sprites('Tiles\\3.png', x + 5, y + 5, self.begin, False)
                    s.image = load('Resources\images\Sprites\Tiles\\1.png')
                    s.rect.x -= 5
                    s.rect.y -= 5
                    self.sprites.add(s)
                else:
                    self.grass.add(Sprites('Tiles\\0.png', x, y, self.begin))
                    if '2' <= self.board[i][j] <= '9':
                        s = Sprites('Tiles\\3.png', x + 5, y + 5, self.begin)
                        s.image = load('Resources\images\Sprites\Tiles\\2.png')
                        s.rect.x -= 5
                        s.rect.y -= 5
                        self.sprites.add(s)
                        if self.board[i][j] != '2':
                            self.bonuses.add(Bonus(x, y, int(self.board[i][j]), self.begin))
                    elif self.board[i][j] == 'P':
                        self.start_pos = (x, y)
                        self.hero = Player(x, y, self.max_bombs, self.strength, self.begin, m * 40, n * 40)
                    elif self.board[i][j] != '0':
                        self.mobs.add(Mobs(self.board[i][j], x, y, 0.9, randint(0, 3), self.begin))
        f.close()
        self.sprites_and_bombs = self.sprites.copy()
        self.start = get_ticks()

    def play(self):
        self.time = get_ticks()
        set_repeat(1, 1)
        is_paused = False
        start_pause = 0
        while not self.end:
            for event in get():
                if event.type == QUIT:
                    exit()
                elif is_paused:
                    if event.type == KEYDOWN and k == 112:
                        is_paused = False
                        self.start = self.start + get_ticks() - start_pause
                        set_repeat(1, 1)
                else:
                    if event.type == KEYDOWN:
                        k = event.key
                        if k == 112:
                            set_repeat(0, 0)
                            is_paused = True
                            start_pause = get_ticks()
                            self.hero.ismoved = False
                            break
                        if k == K_ESCAPE:
                            self.end = True
                            break
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
                            self.hero.place_bomb(self.sprites_and_bombs)
                    elif event.type == KEYUP and event.key != 32:
                        self.hero.ismoved = False
            if not is_paused:
                for m in self.mobs:
                    m.strategy()
                self.time = max(get_ticks(), self.time)
                self.screen.fill(self.color)
                self.grass.update(self.screen)
                self.bonuses.update(self.screen)
                self.sprites.update(self.screen)
                self.hero.update(self.screen, self.sprites)
                self.hero.explosions.update(self.screen)
                self.mobs.update(self.screen, self.sprites_and_bombs)
                self.show_info()
                update()
                killed = False
                for ex in self.hero.explosions:
                    if self.time + 700 < ex.clear_time:
                        for m in self.mobs:
                            if collide_rect(m, ex):
                                self.scores += 15
                                m.kill()
                        for sp in self.sprites:
                            if sp.can and collide_rect(sp, ex):
                                self.scores += 5
                                sp.kill()
                        if collide_rect(self.hero, ex):
                            killed = True
                if killed or self.hero.collide(self.mobs):
                    self.death()
                    if self.end:
                        break
                else:
                    for bon in self.bonuses:
                        if collide_rect(self.hero, bon):
                            if bon.type == 4:
                                self.lives += 1
                            elif bon.type == 5:
                                self.max_bombs += 1
                                self.hero.max_bombs += 1
                            elif bon.type == 6:
                                self.strength += 1
                                self.hero.strength += 1
                            bon.remove(self.bonuses)
                            self.scores += 10
                if len(self.mobs) == 0:
                    self.lvl += 1
                    self.scores += 20
                    self.load_level()

    def death(self):
        self.scores -= 20
        self.lives -= 1
        if self.lives == 0:
            self.lose()
            return
        self.begin[0] = 0
        self.begin[1] = 0
        self.max_bombs = 1
        self.strength = 1
        self.hero = Player(self.start_pos[0], self.start_pos[1], 1, 1, self.begin
                           , len(self.board[0]) * 40, len(self.board) * 40)
        wait(700)
        while spritecollideany(self.hero, self.mobs):
            for m in self.mobs:
                m.strategy()
                m.update(self.screen, self.sprites)
        update()

    def lose(self):
        self.end = True

    def win(self):
        self.scores += 50
        self.end = True

    def update_timer(self):
        s = 180 - (get_ticks() - self.start) // 1000
        if s == 0:
            self.lose()
            return
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

        label = font.render('Scores ' + str(self.scores), True, (255, 180, 0))
        self.screen.blit(label, (590, 5))
        self.update_timer()
