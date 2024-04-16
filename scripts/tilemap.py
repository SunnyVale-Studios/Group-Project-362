import pygame as pg

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1) , (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'} # set
class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.settings = game.settings
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.image = pg.Surface((16, 16), pg.SRCALPHA)
        self.image2 = pg.Surface((16, 16), pg.SRCALPHA)
        self.image.fill((255,255,255))
        self.image2.fill((0, 0, 255))


        for i in range(10):
            self.tilemap[str(3 + i) + ';50'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 50)}
            self.tilemap['10;' + str(50 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 50 + i)}

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pg.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def draw(self, screen, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            screen.blit(self.image2, (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))   

        for x in range(offset[0] // self.tile_size, (offset[0] + self.settings.screen_width) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + self.settings.screen_height) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    screen.blit(self.image, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
