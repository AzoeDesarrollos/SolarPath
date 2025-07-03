from pygame import KEYDOWN, KEYUP, QUIT, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_ESCAPE
from pygame import quit as pg_quit, event, time
from pygame.sprite import LayeredUpdates


class SpriteHandler:
    observer = None

    @classmethod
    def init(cls):
        cls.contents = LayeredUpdates()
        cls.clock = time.Clock()

    @classmethod
    def add_sprite(cls, sprite):
        if sprite.is_observer:
            cls.observer = sprite

        cls.contents.add(sprite)
        sprite.set_parent(cls)

    @classmethod
    def del_sprite(cls, sprite):
        if sprite in cls.contents:
            cls.contents.remove(sprite)

    @classmethod
    def get_sprite(cls, name):
        for sprite in cls.contents.sprites():
            if sprite.name == name:
                return sprite

    @classmethod
    def update(cls):
        delta_time = cls.clock.tick(60) / 1000
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
                    cls.observer.moverse(0, 1)
                elif e.key == K_DOWN:
                    cls.observer.moverse(0, -1)
                elif e.key == K_RIGHT:
                    cls.observer.moverse(1, 0)
                elif e.key == K_LEFT:
                    cls.observer.moverse(1, 0)

            elif e.type == KEYUP:
                if e.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                    cls.observer.moverse(0, 0)

        cls.observer.move(delta_time)
        cls.contents.update()


SpriteHandler.init()