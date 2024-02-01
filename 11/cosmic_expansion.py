import sys

class Galaxy:

    def __init__(self, x, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

class CosmicExpansion:

    def __init__(self, filename, expansion):
        self.galaxies = []
        self.expansion = expansion
        lines = open(filename, 'r').readlines()
        self._load_galaxies(lines)

    def _load_galaxies(self, lines):
        nr_rows = len(lines)
        nr_cols = len(lines[0].rstrip())
        print(f'Initial universe: {nr_rows} x {nr_cols}')
        columns = []
        for i in range(nr_cols):
            columns.append([]) # each column will contain a list of galaxies
        rowidx = 0
        for row in lines:
            row = row.rstrip()
            had_galaxies = False
            for j in range(nr_cols):
                if row[j] == '#':
                    had_galaxies = True
                    galaxy = Galaxy(rowidx)
                    columns[j].append(galaxy)
                    self.galaxies.append(galaxy)
            rowidx += 1 if had_galaxies else self.expansion
        # determine galaxy columns depending on expanded space
        colidx = 0
        for col in columns:
            had_galaxies = False
            for galaxy in col:
                galaxy.y = colidx
                had_galaxies = True
            colidx += 1 if had_galaxies else self.expansion
        print(f'Expanded universe: {rowidx+1} x {colidx+1}')

    def __repr__(self):
        return str(self.galaxies)

    def galaxy_pairs(self):
        nr_galaxies = len(self.galaxies)
        for i in range(nr_galaxies-1):
            for j in range(i+1, nr_galaxies):
                yield self.galaxies[i], self.galaxies[j]

    def galaxy_distances(self):
        return sum(map(
                # due to zigzag movement, distance is not a hypotenuse but a sum of x, y distancies
                lambda pair: abs(pair[0].x - pair[1].x) + abs(pair[0].y - pair[1].y),
                self.galaxy_pairs()))

def main(filename):
    part1 = CosmicExpansion(filename, 2)
    print(f'Sum of distances with 2 expansion: {part1.galaxy_distances()}')
    part2 = CosmicExpansion(filename, 1000000)
    print(f'Sum of distances with 1000000 expansion: {part2.galaxy_distances()}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = 'input.txt'
    else:
        filename = sys.argv[1]
    main(filename)
