from pygame import KEYDOWN, KEYUP, QUIT, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_ESCAPE
from pygame import quit as pg_quit, event
from pygame.sprite import LayeredUpdates


class SpriteHandler:
    observer = None

    @classmethod
    def init(cls):
        cls.contents = LayeredUpdates()

    @classmethod
    def add_sprite(cls, sprite):
        if sprite.is_observer:
            cls.observer = sprite
            cls.observer.parent = SpriteHandler
        else:
            cls.contents.add(sprite)
            sprite.parent = SpriteHandler

    @classmethod
    def del_sprite(cls, sprite):
        if sprite in cls.contents:
            cls.contents.remove(sprite)

    @classmethod
    def update(cls):
        delta_time = cls.observer.delta_time
        dx, dy = cls.observer.x, cls.observer.y  # velocidad horizontal y vertical, respectivamente
        for e in event.get([KEYDOWN, KEYUP, QUIT]):
            if (e.type == KEYDOWN and e.key == K_ESCAPE) or e.type == QUIT:
                pg_quit()
                exit()
            elif e.type == KEYDOWN:
                # if e.key == K_a:
                #     show_arc = not show_arc
                # elif e.key == K_SPACE:
                #     planet_time.time_speed = 0 if planet_time.time_speed > 0 else 3
                # elif e.key == K_r:
                #     planet_time.toggle_mode()
                if e.key == K_UP:
                    dy += 1
                elif e.key == K_DOWN:
                    dy -= 1
                elif e.key == K_RIGHT:
                    dx += 1
                elif e.key == K_LEFT:
                    dx -= 1

            elif e.type == KEYUP:
                if e.key in (K_UP, K_DOWN):
                    dy = 0
                elif e.key in (K_LEFT, K_RIGHT):
                    dx = 0

        cls.observer.move(dx, dy)
        # latitude_deg += dy * 10 * delta_time

        cls.contents.update(delta_time)


SpriteHandler.init()