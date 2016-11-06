from datetime import datetime, timedelta
import math
import random

from constants import DEFAULT_CHARACTER_NAME, DEFAULT_WORLD_SIZE
from world import World


class Character:

    def __init__(self, name=DEFAULT_CHARACTER_NAME, x=0, y=0):
        self.name = name
        self.x, self.y = x, y


class Game:

    def __init__(self, seed=None, n_characters=5):
        if seed is None:
            seed = random.Random()
        self.seed = seed
        self.world = World(width=DEFAULT_WORLD_SIZE, height=DEFAULT_WORLD_SIZE, seed=self.seed)
        self.characters = self.generate_characters(n_characters)
        self.creation_time = datetime.now()
        self.game_duration = timedelta(microseconds=0)

    def generate_characters(self, n_characters):
        characters = []
        for i in range(n_characters):
            character = Character(x=random.randint(0, self.world.width - 1),
                                  y=random.randint(0, self.world.height - 1),
                                  name='Dummy #{}'.format(i))
            characters.append(character)
        return characters

    def update(self, dt):
        self.game_duration = datetime.now() - self.creation_time
        sine = math.sin(self.game_duration.microseconds / 200000.)
        for character in self.characters:
            if hash(character.name) % 2:
                character.x += 0.15 * sine
            else:
                character.y += 0.15 * sine
