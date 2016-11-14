
import random

import cocos
from cocos.tiles import TileSet, RectCell, RectMapLayer
from cocos.director import director
from cocos.layer.scrolling import ScrollingManager
import pyglet

from game import Game
from views import WorldMap

class MainGame:
    def __init__(self, width, height):
        # World/map management
        self.seed = random.Random()
        self.game = Game(seed=self.seed)

    def run(self):
        director.init(resizable=True, autoscale=False)
        scroller = ScrollingManager()
        scroller.add(WorldMap(self.game.world))
        main_scene = cocos.scene.Scene(scroller)
        director.run(main_scene)

if __name__ == '__main__':
    main_game = MainGame(1080, 960)
    main_game.run()
