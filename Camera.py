from pygame import Rect

class Camera:
    def __init__(self, width, height):
        self.state = Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(target.rect)

    def camera_func(self, target_rect):
        l = -target_rect.x + 1024 / 2
        t = -target_rect.y + 768 / 2
        w, h = self.width, self.height

        l = min(0, l)
        l = max(-(w - 1024), l)
        t = max(-(h - 768), t)
        t = min(0, t)
        return Rect(l, t, w, h)
