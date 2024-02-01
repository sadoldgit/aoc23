import sys
# coordinate system
# 0 x->
# y
# |
# v

North = (0,-1)
East = (1,0)
South = (0,1)
West = (-1,0)

class Tile:
    " "
    connects = {}

    def __init__(self, x, y):
        self.x = x
        self.y = y
        #part 2
        self.on_loop = False

    def __repr__(self):
        return self.__doc__

    def go(self, tile_from):
        side_from = (tile_from.x - self.x, tile_from.y - self.y)
        return self.x + self.connects[side_from][0], self.y + self.connects[side_from][1]

class NS(Tile):
    "|"
    connects = {North:South, South:North}
    symbol = '|'

    def __init__(self, x, y):
        super().__init__(x, y)

class EW(Tile):
    "-"
    connects = {East:West, West:East}

    def __init__(self, x, y):
        super().__init__(x, y)

class NE(Tile):
    "L"
    connects = {North:East, East:North}

    def __init__(self, x, y):
        super().__init__(x, y)

class NW(Tile):
    "J"
    connects = {North:West, West:North}

    def __init__(self, x, y):
        super().__init__(x, y)

class SW(Tile):
    "7"
    connects = {South:West, West:South}

    def __init__(self, x, y):
        super().__init__(x, y)

class SE(Tile):
    "F"
    connects = {South:East, East:South}

    def __init__(self, x, y):
        super().__init__(x, y)

class Gnd(Tile):
    "."

    def __init__(self, x, y):
        super().__init__(x, y)

class Start(Tile):
    "S"

    def __init__(self, x, y):
        super().__init__(x, y)


tile_factory = {scls.__doc__:scls for scls in Tile.__subclasses__()}

class PipeMaze:

    def __init__(self, filename):
        self.maze = []
        x = 0
        y = 0
        self.start_tile = None
        with open(filename, 'r') as f:
            for line in f.readlines():
                line = list(line.rstrip())
                row = []
                for x in range(len(line)):
                    tile = tile_factory[line[x]](x, y)
                    row.append(tile)
                    if type(tile) is Start:
                        self.start_tile = tile
                self.maze.append(row)
                y += 1
        self.first_tiles = self._get_first_tiles()
        # part 2
        self.start_tile.on_loop = True
        self.first_tiles[0].on_loop = True
        self.first_tiles[1].on_loop = True

    def __repr__(self):
        return '\n'.join(''.join(str(tile) for tile in row) for row in self.maze)

    def _get_first_tiles(self):
        "..the ones around the start tile, having an entry from it"
        # simply try to go from the start tile -> no exception if it has an entry there
        first_tiles = []
        for x in range(-1, 2):
            for y in range (-1, 2):
                if x == y and x == 0:
                    continue
                try:
                    # should have checked if this is inside the maze area.. but we know it is :)
                    tile = self.maze[self.start_tile.y + y][self.start_tile.x + x]
                    _ = tile.go(self.start_tile)
                    first_tiles.append(tile)
                except:
                    pass
        return first_tiles

    def walk(self, next_tile, comming_from):
        while type(next_tile) is not Start:
            next_x, next_y = next_tile.go(comming_from)
            comming_from = next_tile
            next_tile = self.maze[next_y][next_x]
            next_tile.on_loop = True # part 2
            yield next_tile

    def part1_farthest_steps(self):
        distance = 1
        path1 = self.walk(self.first_tiles[0], self.start_tile)
        path2 = self.walk(self.first_tiles[1], self.start_tile)
        pos1 = next(path1)
        pos2 = next(path2)
        while pos1 != pos2:
            distance += 1
            pos1 = next(path1)
            pos2 = next(path2)
        return distance + 1 # meeting point

    def part2_loop_area(self):
        # approach: scan rows, from left to right
        # point can be inside of loop if we crossed a path
        # and then again once more. (we are not crossing if we are on path)
        # NOT GOOD: detect moving along the path and crossing the path
        area = 0
        for row in self.maze:
            prev_tile = None
            candidate = 0
            for tile in row:
                if (candidate == 0
                    and not tile.on_loop
                    and prev_tile is not None
                    and prev_tile.on_loop):
                        candidate = 1
                elif (candidate > 0
                    and not tile.on_loop):
                    candidate += 1
                elif (candidate > 0
                    and tile.on_loop):
                        area += candidate
                        candidate = 0
                prev_tile = tile
        return area


def main(filename):
    game = PipeMaze(filename)
    distance = game.part1_farthest_steps() # 6682
    area = game.part2_loop_area()
    print(distance, area)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = 'test1.txt'
    else:
        filename = sys.argv[1]
    main(filename)
