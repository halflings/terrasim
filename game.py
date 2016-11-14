from datetime import datetime, timedelta
import random

from constants import DEFAULT_CHARACTER_NAME, DEFAULT_WORLD_SIZE, DEFAULT_NUMBER_CHARACTERS
from world import World


class Character:

    def __init__(self, name=DEFAULT_CHARACTER_NAME, x=0, y=0):
        self.name = name
        self.x, self.y = x, y
        self.goal = None

    def update(self, dt):
        if self.goal is None:
            return
        self.x += (self.goal[0] - self.x) * dt
        self.y += (self.goal[1] - self.y) * dt
        if (self.x - self.goal[0])**2 + (self.y - self.goal[1])**2 < 0.1:
            # Goal reached
            self.x, self.y = self.goal
            self.goal = None


class Game:

    def __init__(self, seed=None, world_width=DEFAULT_WORLD_SIZE, world_height=DEFAULT_WORLD_SIZE,
                 n_characters=DEFAULT_NUMBER_CHARACTERS):
        if seed is None:
            seed = random.Random()
        self.seed = seed
        self.world = World(width=world_width, height=world_height, seed=self.seed)
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
        for character in self.characters:
            character.update(dt)
            # Setting a random goal, for debugging only.
            if character.goal is None:
                character.goal = (
                    random.randint(0, self.world.width - 1),
                    random.randint(0, self.world.height - 1))
