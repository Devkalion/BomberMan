from pygame import display, Rect
from pygame.sprite import Sprite, collide_rect, Group
from pygame.time import get_ticks
from pygame.image import load
from random import randint


class Sprites(Sprite):
    def __init__(self, screen, file_name, x, y):
        Sprite.__init__(self)
        self.image = load('Resources\images\Sprites\\' + file_name)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.rect.y += y

    def update(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))


class Mobs(Sprites):
    def __init__(self, screen, file_name, x, y, speed=0.8, dir=0):
        Sprites.__init__(self, screen, file_name + '_down.png', x, y)
        self.speed = speed
        self.dir = dir
        self.dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.x = x - self.rect.x
        self.y = y - self.rect.y
        #self.x = x - self.rect.x
        #self.y = x - self.rect.y
        #print(self.x, self.y)
        self.load_imgs(file_name)

    def load_imgs(self, file_name):
        self.imgs = [load('Resources\images\Sprites\\' + file_name + '_down.png'),
                     load('Resources\images\Sprites\\' + file_name + '_up.png'),
                     load('Resources\images\Sprites\\' + file_name + '_right.png'),
                     load('Resources\images\Sprites\\' + file_name + '_left.png')]
        self.image = self.imgs[self.dir]

    def rotate(self, new_dir):
        self.dir = new_dir
        self.image = self.imgs[self.dir]

    def strategy(self):
        if not randint(0, 250):
            self.rotate(randint(0, 3))
        if not randint(0, 1):
            self.ismoved = True
            return
        self.ismoved = False

    def update(self, sprites):
        if self.ismoved:
            (dx, dy) = self.dirs[self.dir]
            if dx != 0:
                self.x += dx * self.speed
                self.rect.x += self.x
                self.x = self.x % 1
            else:
                self.y += dy * self.speed
                self.rect.y += self.y
                self.y = self.y % 1
            self.collide(sprites)
        self.screen.blit(self.image, (self.rect.x + self.x, self.rect.y + self.y))

    def collide(self, sprites):
        for sp in sprites:
            if collide_rect(self, sp):
                if self.dir == 0:
                    self.rect.bottom = sp.rect.top
                elif self.dir == 1:
                    self.rect.top = sp.rect.bottom
                elif self.dir == 2:
                    self.rect.right = sp.rect.left
                elif self.dir == 3:
                    self.rect.left = sp.rect.right


class Player(Mobs):
    def __init__(self, screen, x, y, max_bombs, strength):
        Mobs.__init__(self, screen, 'Player\p', x, y, 0.7)
        self.max_bombs = max_bombs
        self.strength = strength
        self.bombs = Group()
        self.explosions = Group()

    def place_bomb(self):
        if len(self.bombs) < self.max_bombs:
            (x, y) = self.rect.x, self.rect.y
            x = (x + 20) // 40 * 40
            y = (y + 20) // 40 * 40 + 10
            self.bombs.add(Bomb(self.screen, x, y, self.strength))

    def update(self, sprites, ismoved):
        self.ismoved = ismoved
        Mobs.update(self, sprites)
        for ex in self.explosions:
            if ex.clear_time <= get_ticks():
                ex.kill()
            else:
                break
        for b in self.bombs:
            if get_ticks() >= b.explosion_time:
                clock = get_ticks()
                dirs = self.dirs
                for j in range(b.strength + 1):
                    if j > 0:
                        for dir in dirs:
                            (x, y) = b.rect.x, b.rect.y
                            x += dir[0] * 40 * j
                            y += dir[1] * 40 * j
                            exp = Explosion(b.screen, x, y, clock)
                            ok = True
                            for sp in sprites:
                                if collide_rect(exp, sp):
                                    ok = False
                                    break
                            if ok:
                                self.explosions.add(exp)
                    else:
                        self.explosions.add(Explosion(b.screen, b.rect.x, b.rect.y, clock))
                b.kill()
            else:
                b.update()
        self.explosions.update()


class Bomb(Sprites):
    def __init__(self, screen, x, y, strength):
        Sprites.__init__(self, screen, 'Player\\bomb.png', x, y)
        self.explosion_time = get_ticks() + 1500
        self.strength = strength


class Explosion(Sprites):
    def __init__(self, screen, x, y, time):
        Sprites.__init__(self, screen, 'Player\\explosion.png', x, y)
        self.clear_time = time + 800
