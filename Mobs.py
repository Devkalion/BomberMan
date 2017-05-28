from pygame.sprite import Sprite, collide_rect, Group, spritecollideany
from pygame.time import get_ticks
from pygame.image import load
from random import randint


class Sprites(Sprite):
    def __init__(self, file_name, x, y, l, can=True):
        Sprite.__init__(self)
        self.can = can
        self.image = load('Resources\images\Sprites\\' + file_name)
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.l = l
        self.rect.y += y

    def update(self, screen):
        screen.blit(self.image, (self.rect.x - self.l[0], self.rect.y - self.l[1]))


class Bomb(Sprites):
    def __init__(self, x, y, strength, l):
        Sprites.__init__(self, 'Player\\bomb.png', x, y, l)
        self.explosion_time = get_ticks() + 1500
        self.strength = strength


class Explosion(Sprites):
    def __init__(self, x, y, time, l):
        Sprites.__init__(self, 'Player\\explosion.png', x, y, l)
        self.clear_time = time + 800


class Bonus(Sprites):
    def __init__(self, x, y, type, l):
        Sprites.__init__(self, 'Player\\bonus' + str(type) + '.png', x, y, l)
        self.type = type


class Mobs(Sprites):
    def __init__(self, file_name, x, y, speed=1, dir=0, l=None):
        Sprites.__init__(self, file_name + '_down.png', x, y, l)
        self.ismoved = False
        self.speed = speed
        self.dir = dir
        self.dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.x = x - self.rect.x
        self.y = y - self.rect.y
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
        if not randint(0, 125):
            self.rotate(randint(0, 3))
        if not randint(0, 1):
            self.ismoved = True
            return
        self.ismoved = False

    def update(self, screen, sprites=Group()):
        if self.ismoved:
            (dx, dy) = self.dirs[self.dir]
            if dx != 0:
                self.x += dx * self.speed
                self.rect.x += self.x
                self.x %= 1
            else:
                self.y += dy * self.speed
                self.rect.y += self.y
                self.y %= 1
            self.collide(sprites)
        Sprites.update(self, screen)

    def collide(self, sprites):
        ans = False
        for sp in sprites:
            if collide_rect(self, sp):
                ans = True
                if self.dir == 0:
                    self.rect.bottom = sp.rect.top
                elif self.dir == 1:
                    self.rect.top = sp.rect.bottom
                elif self.dir == 2:
                    self.rect.right = sp.rect.left
                elif self.dir == 3:
                    self.rect.left = sp.rect.right
        return ans


class Player(Mobs):
    def __init__(self, x, y, max_bombs, strength, l, width, height):
        Mobs.__init__(self, 'Player\p', x, y, 1.5, 0, l)
        self.width = width
        self.height = height
        self.max_bombs = max_bombs
        self.strength = strength
        self.bombs = Group()
        self.explosions = Group()
        self.bombs_on_ground = set()
        self.pr_tick = get_ticks()

    def place_bomb(self, group):
        time = get_ticks()
        if len(self.bombs_on_ground) < self.max_bombs:
            if self.pr_tick + 150 < time:
                self.pr_tick = time
                (x, y) = self.rect.x, self.rect.y
                x = (x + 20) // 40 * 40
                y = (y + 20) // 40 * 40 + 10
                k = len(self.bombs_on_ground)
                self.bombs_on_ground.add((x, y))
                if k != len(self.bombs_on_ground):
                    b = Bomb(x, y, self.strength, self.l)
                    self.bombs.add(b)
                    group.add(b)

    def update(self, screen, sprites):
        Mobs.update(self, screen, sprites)
        while self.rect.x - self.l[0] > 512 and self.rect.x + 512 < self.width:
            self.l[0] += 1
        while self.rect.x - self.l[0] < 512 and self.rect.x - 512 > 0:
            self.l[0] -= 1
        while self.rect.y - self.l[1] > 359 and self.rect.y + 359 < self.height:
            self.l[1] += 1
        while self.rect.y - self.l[1] < 359 and self.rect.y - 359 > 0:
            self.l[1] -= 1
        for ex in self.explosions:
            if ex.clear_time <= get_ticks():
                ex.kill()
            else:
                break
        for b in self.bombs:
            if get_ticks() >= b.explosion_time or spritecollideany(b, self.explosions):
                clock = get_ticks()
                dirs = self.dirs.copy()
                (x, y) = b.rect.x, b.rect.y
                for j in range(b.strength + 1):
                    if j > 0:
                        i = 0
                        while i < len(dirs):
                            dir = dirs[i]
                            i += 1
                            dx = x + dir[0] * 40 * j
                            dy = y + dir[1] * 40 * j
                            exp = Explosion(dx, dy, clock, self.l)
                            ok = True
                            for sp in sprites:
                                if collide_rect(exp, sp):
                                    dirs.remove(dir)
                                    ok = sp.can
                                    i -= 1
                                    break
                            if ok:
                                self.explosions.add(exp)
                    else:
                        self.explosions.add(Explosion(b.rect.x, b.rect.y, clock, self.l))
                self.bombs_on_ground.remove((x, y))
                b.kill()
            else:
                b.update(screen)
