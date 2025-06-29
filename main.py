from globs import Renderer, SpriteHandler, HEIGHT
from sun import Planet, Star, Observer

planet = Planet(HEIGHT // 2 + 100)
star = Star(8)

Renderer.add_sprite(planet)
# Renderer.add_sprite(star)
SpriteHandler.add_sprite(planet)
# SpriteHandler.add_sprite(star)
Observer.init()
SpriteHandler.add_sprite(Observer)

while True:
    SpriteHandler.update()
    Renderer.update()