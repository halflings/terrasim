from datetime import datetime, timedelta

from constants import DEFAULT_CHARACTER_NAME, DEFAULT_WORLD_SIZE
from world import World


class Character:

    def __init__(self, name=DEFAULT_CHARACTER_NAME):
        self.name = name
        self.x = self.y = 0


class Game:

    def __init__(self):
        self.world = World(width=DEFAULT_WORLD_SIZE, height=DEFAULT_WORLD_SIZE)
        self.character = Character()
        self.creation_time = datetime.now()
        self.game_duration = timedelta(microseconds=0)

    def update(self, dt):
        self.game_duration = datetime.now() - self.creation_time
