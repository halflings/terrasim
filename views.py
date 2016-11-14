import cocos
import pyglet

from world import Terrain

TERRAIN_TEXTURES = {Terrain.GRASS: 'grass.png', Terrain.DIRT: 'dirt.png',
                    Terrain.WATER: 'water.png', Terrain.MOUNTAIN: 'mountain.png'}
CELL_SIZE = 32
DEFAULT_CHARACTER = pyglet.resource.image('res/img/dummy.png')


class WorldMap(cocos.tiles.RectMapLayer):

    def __init__(self, world, id=None):
        self.world = world
        cells = self._generate_cells(world, cell_size=CELL_SIZE)
        super(WorldMap, self).__init__(id=None, tw=CELL_SIZE, th=CELL_SIZE, cells=cells)

    def _generate_cells(self, world, cell_size):
        tileset = cocos.tiles.TileSet(0, None)
        for cell_type in list(Terrain):
            image_path = 'res/img/tiles/{}'.format(TERRAIN_TEXTURES[cell_type])
            image = pyglet.resource.image(image_path)
            tileset.add(image=image, id=cell_type, properties={})

        cells = []
        for i in range(world.width):
            column = []
            for j in range(world.height):
                tile = tileset[world.cells[i][j]]
                cell = cocos.tiles.RectCell(i, j, cell_size, cell_size, properties={}, tile=tile)
                column.append(cell)
            cells.append(column)
        return cells

class CharacterView2(cocos.layer.ScrollableLayer):
    def __init__(self, character):
        super(CharacterView2, self).__init__()
        self.character = character
        self.add(cocos.sprite.Sprite(DEFAULT_CHARACTER,
                                     position=(character.x * CELL_SIZE,
                                               character.y * CELL_SIZE),
                                     anchor=(CELL_SIZE / 2, CELL_SIZE / 2)
                                     ))


# All the views below are from the old pyglet version and should be removed.

class WorldView:

    def __init__(self, window, world):
        self.window = window
        self.world = world
        self.textures = {terrain_type:
            pyglet.resource.image('res/img/tiles/{}'.format(TERRAIN_TEXTURES[terrain_type]))
            for terrain_type in list(Terrain)}
        self.cursor_position = None
        self.selected_cell = None
        self.map_sprites = []
        self.batch = pyglet.graphics.Batch()

    def set_cursor_position(self, x, y):
        self.cursor_position = (x, y)
        self.selected_cell = (x // CELL_SIZE, y // CELL_SIZE)

    def generate_sprites(self):
        min_x = max(0, self.window.x // CELL_SIZE)
        min_y = max(0, self.window.y // CELL_SIZE)
        view_cell_width = (self.window.width // CELL_SIZE) + 1
        view_cell_height = (self.window.height // CELL_SIZE) + 1
        max_x = min(min_x + view_cell_width, self.world.width - 1)
        max_y = min(min_y + view_cell_height, self.world.height - 1)

        map_sprites = []
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                sprite = pyglet.sprite.Sprite(
                    self.textures[self.world.cells[x][y]], x=x * CELL_SIZE,
                    y=y * CELL_SIZE, batch=self.batch)
                map_sprites.append(sprite)
        return map_sprites

    def draw(self):
        # This generates the sprites using the current batch
        self.map_sprites = self.generate_sprites()
        self.batch.draw()

    def draw_selected_cell(self):
        # TODO: make this use a batch?
        # Drawing rectangle around the currently selected cell
        if self.selected_cell is not None:
            x, y = self.selected_cell[0] * CELL_SIZE, self.selected_cell[1] * CELL_SIZE
            dx = dy = CELL_SIZE
            vertices = [x, y, x + dx, y, x + dx, y + dy, x, y + dy]
            pyglet.graphics.draw(
                4, pyglet.gl.GL_LINE_LOOP, ('v2f', vertices),
                ('c3B', (0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255, 255)))


class CharacterView:


    def __init__(self, window, batch, character):
        self.window = window
        self.character = character
        self.sprite = pyglet.sprite.Sprite(
            img=DEFAULT_CHARACTER, x=self.character.x, y=self.character.y, batch=batch)

    def draw(self):
        x = self.character.x * CELL_SIZE
        y = self.character.y * CELL_SIZE
        self.sprite.x = x
        self.sprite.y = y
        if self.character.goal is not None:
            goal_x = self.character.goal[0] * CELL_SIZE
            goal_y = self.character.goal[1] * CELL_SIZE
            vertices = [x, y, goal_x, goal_y]
            vertices = [v + CELL_SIZE / 2 for v in vertices]
            pyglet.graphics.draw(
                2, pyglet.gl.GL_LINES, ('v2f', vertices), ('c4B', (255, 255, 255, 125) * 2))


class CharactersView:

    def __init__(self, window, game):
        self.window = window
        self.batch = pyglet.graphics.Batch()
        self.game = game
        self.cur_characters = set(self.game.characters)
        self.views = self._generate_views(self.cur_characters)

    def draw(self):
        if self.cur_characters != set(self.game.characters):
            self.cur_characters = set(self.game.characters)
            self.character_views = self._generate_views(self.cur_characters)

        for view in self.views:
            view.draw()
        self.batch.draw()

    def _generate_views(self, characters):
        return [CharacterView(self.window, self.batch, c) for c in characters]
