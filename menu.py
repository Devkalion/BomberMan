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
        self.bg_color = Color('#153515')
        self.load_images()
        self.btns = [(70, 490, 182, 552), (70, 555, 334, 602), (70, 620, 351, 681), (70, 685, 168, 733)]
        self.checked_btn = 0
        self.reload()
        self.cycle()

    def load_images(self):
        self.logo = load('Resources\images\logo.png')
        self.play = load('Resources\images\Buttons\Play.png')
        self.instructions_btn = load('Resources\images\Buttons\Instructions.png')
        self.highscores = load('Resources\images\Buttons\High Scores.png')
        self.exit = load('Resources\images\Buttons\Exit.png')
        self.man = load('Resources\images\man.png')
        self.submenu = Surface((50, 236))
        self.submenu.fill(self.bg_color)
        self.explosion = load('Resources\images\Explosion.png')
        self.bomb = load('Resources\images\\bomb.png')
        self.back = load('Resources\images\Buttons\Back.png')
        self.img1 = load('Resources\images\img1.png')

    def read_scores(self):
        f = open('Resources\Scores.txt', 'a+')
        f.seek(0)
        self.tabl = [(s.split('~')[0], int(s.split('~')[1])) for s in f.readlines()]
        f.close()

    def reload(self):
        self.screen.fill(Color('#153515'))
        self.screen.blit(self.play, (70, 490))
        self.screen.blit(self.instructions_btn, (70, 555))
        self.screen.blit(self.highscores, (70, 620))
        self.screen.blit(self.exit, (70, 685))
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
        self.screen.blit(self.submenu, (20, 490))
        self.screen.blit(self.bomb, (20, btn[1] + 2))
        update()

    def pressed(self, idx, btn):
        self.screen.blit(self.submenu, (20, 524))
        self.screen.blit(self.explosion, (20, btn[1] + 4))
        update()
        if idx != 3:
            delay(200)
        if idx == 0:
            scores = Play(self.screen, self.bg_color).scores
            if 'tabl' not in self.__dict__:
                self.read_scores()
            new_record = len(self.tabl) < 10
            if not new_record:
                for (name, score) in self.tabl:
                    if score < scores:
                        new_record = True
                        break
            if new_record:
                self.update_scores(scores)
        elif idx == 1:
            self.instructions()
        elif idx == 2:
            if 'tabl' not in self.__dict__:
                self.read_scores()
            self.scores()
        else:
            exit()
        self.reload()

    def update_scores(self, score):
        self.tabl.append(('_', score))
        self.tabl = sorted(self.tabl, key=lambda x: -x[1])[0:(min(len(self.tabl), 10))]
        i = self.tabl.index(('_', score))
        self.print_scores()
        s = ''
        filled = False
        ex = False
        while not filled:
            for event in get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        filled = True
                        self.tabl[i] = (s, self.tabl[i][1])
                        break
                    elif (event.key == 32 or 'a' <= chr(event.key) <= 'z') and len(s) < 8:
                        s1 = chr(event.key)
                        s += s1
                        if len(s) == 8:
                            s1 = s
                        else:
                            s1 = s + '_'
                        self.tabl[i] = (s1, self.tabl[i][1])
                        self.print_scores()
                    elif event.key == 8:
                        s = s[0:len(s) - 1]
                        self.tabl[i] = (s + '_', self.tabl[i][1])
                        self.print_scores()
                    elif event.key == 13:
                        filled = True
                        self.tabl[i] = (s, self.tabl[i][1])
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    filled = True
                    self.tabl[i] = (s, self.tabl[i][1])
                elif event.type == QUIT:
                    ex = True
                    filled = True
                    self.tabl[i] = (s, self.tabl[i][1])
        f = open('Resources\Scores.txt', 'w')
        for k in self.tabl:
            f.write('%s~%d\n' % k)
        f.close()
        if ex:
            exit()
        self.scores()

    def print_scores(self):
        self.screen.fill(Color('#153515'))
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

    def scores(self):
        self.print_scores()
        ok = True
        while ok:
            for event in get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    ok = False
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    [x, y] = event.pos
                    if 50 <= x <= 168 and 690 <= y <= 739:
                        ok = False
                elif event.type == QUIT:
                    exit()

    def instructions(self):
        pass
