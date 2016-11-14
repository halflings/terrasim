import enum
import random


class Terrain(enum.IntEnum):
    WATER = 0
    DIRT = 1
    GRASS = 2
    MOUNTAIN = 3


class World(object):

    def __init__(self, width, height, seed=None):
        self.width, self.height = width, height
        self.rand = random.Random()
        if seed is not None:
            self.rand.seed(seed)
        self.cells = self._generate_map(width, height)

    def _generate_map(self, width, height):
        cells = [[Terrain.WATER for j in range(width)] for i in range(height)]
        num_land_clusters = max(1, int(self.rand.gauss(mu=4, sigma=2)))
        print("num_clusters={}".format(num_land_clusters))
        land_clusters = []
        for _ in range(num_land_clusters):
            cluster = self.rand.randint(0, self.width - 1), self.rand.randint(0, self.width - 1)
            land_clusters.append(cluster)
            x_radius = self.rand.gauss(mu=self.width * 0.2, sigma=self.width * 0.1)
            y_radius = self.rand.gauss(mu=self.height * 0.2, sigma=self.height * 0.1)
            for x in range(cluster[0] - int(x_radius), cluster[0] + int(x_radius)):
                for y in range(cluster[1] - int(y_radius), cluster[1] + int(y_radius)):
                    x, y = self.__snap_point(x, y)
                    if x > self.rand.gauss(mu=self.width * 0.2, sigma=self.width * 0.1) and y > self.rand.gauss(mu=self.height * 0.2, sigma=self.height * 0.1):
                        cells[y][x] = Terrain.DIRT
        return cells

    def __snap_point(self, x, y):
        return min(self.width - 1, max(0, x)), min(self.height - 1, max(0, y))

    def __str__(self):
        return '\n'.join('|'.join(c.name[0] if c != Terrain.WATER else ' ' for c in row) for row in self.cells)


if __name__ == '__main__':
    world = World(width=40, height=20)
    print(str(world))
