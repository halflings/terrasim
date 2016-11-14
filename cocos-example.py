
import random

import cocos
from cocos.tiles import TileSet, RectCell, RectMapLayer
from cocos.director import director
from cocos.layer.scrolling import ScrollingManager
import pyglet

from game import Game
from views import WorldMap, CharacterView2

class MainLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(MainLayer, self).__init__()
        # World/map management
        self.seed = random.Random()
        self.game = Game(seed=self.seed, world_width=30, world_height=15)
        
        # Children
        scroller = ScrollingManager()
        scroller.add(WorldMap(self.game.world))
        for character in self.game.characters:
            scroller.add(CharacterView2(character))
        self.add(scroller)

        self.schedule(self.update)

    def update(self, dt):
        self.game.update(dt)

    def on_key_press(self, symbol, modifiers):
        print("Pressed " + str(symbol))

if __name__ == '__main__':
    director.init(width=800, height=600, resizable=False, autoscale=False)
    director.set_show_FPS(True)
    
    main_layer = MainLayer()
    main_scene = cocos.scene.Scene(main_layer)

    director.run(main_scene)
