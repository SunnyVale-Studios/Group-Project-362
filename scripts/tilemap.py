import pygame as pg 
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1) , (0, 1), (1, 1)]
PHYSICS_TILES = {'platform', 'climbable', 'oneway'} # set
class Tilemap:
    def __init__(self, game, platformLevel, climbableLevel, onewayLevel, tile_size=16):
        self.game = game
        self.settings = game.settings
        self.tile_size = tile_size
        self.tilemap = {} # Here will be the player level
        self.platformLevel = platformLevel
        self.climbableLevel = climbableLevel
        self.onewayLevel = onewayLevel
        self.image = pg.Surface((16, 16), pg.SRCALPHA)
        self.image.fill((255,255,255))

        for tile in platformLevel:
            if tile[2] != 0:
                self.tilemap[str(tile[0]) + ';' + str(tile[1])] = {'type': 'platform', 'pos': (tile[0], tile[1])}
        for tile in onewayLevel:
            if tile[2] != 0:
                self.tilemap[str(tile[0]) + ';' + str(tile[1])] = {'type': 'oneway', 'pos': (tile[0], tile[1])}
        for tile in climbableLevel:
            if tile[2] != 0:
                self.tilemap[str(tile[0]) + ';' + str(tile[1])] = {'type': 'climbable', 'pos': (tile[0], tile[1])}

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
            if tile['type'] == 'platform' or tile['type'] == 'oneway':  # Only include platform tiles for collision
                rects.append(pg.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def oneway_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] == 'oneway' and not tile['type'] == 'climbable':
                rects.append(pg.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size , self.tile_size, self.tile_size))
        return rects

    def draw(self, screen, offset=(0, 0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + self.settings.screen_width) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + self.settings.screen_height) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    screen.blit(self.image, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

if __name__ == "__main__":
    print("Incorrect file ran! Run python3 game.py")   

