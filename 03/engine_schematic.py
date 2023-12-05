import re
import sys

class Part:

    def __init__(self, linenr, pos_start, pos_end, lines):
        self.linenr = linenr
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.part_num = int(lines[linenr][pos_start:pos_end])
        self.engine_lines = lines

    def __repr__(self):
        return f'{self.part_num} from {self.pos_start} to {self.pos_end}'

    def _left(self):
        return max(0, self.pos_start - 1)

    def _right(self):
        return min(self.pos_end + 1, len(self.engine_lines[self.linenr]))

    def borders(self):
        top = self.linenr - 1
        bottom = self.linenr + 1
        borders = ''
        if self.linenr > 0:
            borders += f'{self.engine_lines[top][self._left():self._right()]}\n'
        borders += f'{self.engine_lines[self.linenr][self._left():self._right()]}\n'
        if self.linenr < len(self.engine_lines) - 1:
            borders += f'{self.engine_lines[bottom][self._left():self._right()]}'
        return borders

    def is_adjecent_to_symbol(self):
        borders = self.borders().replace('\n','')
        return any(filter(lambda c: not c.isdigit() and not c == '.', borders))

    def possible_gears(self):
        gears = []
        for i in range(max(self.linenr - 1, 0), min(len(self.engine_lines), self.linenr + 2)):
            startx = self._left()
            x = [(startx + m.start(), i) for m in
                 re.finditer('\*', self.engine_lines[i][startx:self._right()])]
            gears.extend(x)
        return gears

class EngineSchematic:

    def __init__(self, filename):
        self.lines = [line.rstrip() for line in open(filename, 'r').readlines()]
        self.schema = []
        self._get_schematic()

    def _get_schematic(self):
        for i in range(0, len(self.lines)):
            line = self.lines[i]
            parts = [Part(i, m.start(), m.end(), self.lines) for m in re.finditer('[0-9]+', line)]
            self.schema.append(parts)

    def __repr__(self):
        return ''.join(repr(self.schema))

    def part1_sum_part_numbers(self):
        parts_sum = 0
        for i in range(0, len(self.schema)):
            for part in self.schema[i]:
                if part.is_adjecent_to_symbol():
                    parts_sum += part.part_num
        return parts_sum

    def part2_gear_ratio(self):
        gear_ratio = 0
        gears = {}
        for i in range(0, len(self.schema)):
            for part in self.schema[i]:
                for gear in part.possible_gears():
                    gearhash = 1000 * gear[0] + gear[1]
                    if gearhash in gears:
                        gears[gearhash].append(part)
                    else:
                        gears[gearhash] = [part]
        sum_ratio = 0
        for _, v in gears.items():
            if len(v) == 2:
                sum_ratio += v[0].part_num * v[1].part_num
        return sum_ratio

def main(filename):
    engine = EngineSchematic(filename)
    print(engine.part1_sum_part_numbers())
    print(engine.part2_gear_ratio())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = 'input.txt'
    else:
        filename = sys.argv[1]
    main(filename)
