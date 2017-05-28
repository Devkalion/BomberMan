from random import randint

f = open('level_tmp.txt', 'w')
h = randint(15, 21)
w = randint(21, 41)
if h % 2 == 0:
    h += 1
if w % 2 == 0:
    w += 1
for i in range(h):
    s = ''
    for j in range(w):
        if i == 0 or j == 0 or i == h - 1 or j == w - 1 or i % 2 == 0 and j % 2 == 0:
            s += '1'
        elif i == 1 and j == 1:
            s += 'P'
        elif randint(0, 1):
            s += '2'
        else:
            s += '0'
    f.write(s + '\n')
f.close()