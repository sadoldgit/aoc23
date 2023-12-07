import re
import sys
# warn: input data has to be manually prepared:
import data
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Range:

    def __init__(self, src, dest, span):
        self.src  = src
        self.dest = dest
        self.span = span

    def __repr__(self):
        return f'Range({self.src}, {self.dest}, {self.span})'

    def __gt__(self, other):
        """helps getting max range for the wanted src"""
        return self.src > other.src

    def get_dest(self, src):
        """get the destination for the given source"""
        return self.dest + (src - self.src)

    @property
    def maxdest(self):
        return self.dest + self.span

class Depends:

    def __init__(self, name):
        self.name = name
        self.data = None
        self.ranges = []

    def read_data(self, maplist):
        """input data in the format [[dest1, src1, span1], [dest2, src2, span2],..]"""
        self.data = sorted(maplist, key=lambda row: row[1])
        # no definition for range 0-
        if self.data[0][1] != 0:
            self.ranges.append(Range(0, 0, self.data[0][1]))
        rows = len(self.data)
        for i in range(0, rows):
            dst, src, span = self.data[i]
            self.ranges.append(Range(src, dst, span))
            if i == rows - 1:
                continue
            _, srcnext, _ = self.data[i+1]
            if src + span < srcnext:
                newsrc = src + span
                self.ranges.append(Range(newsrc, newsrc, srcnext - newsrc))

    def __repr__(self):
        return str(self.ranges)

    def _range(self, src) -> Range:
        """find range for the given src"""
        return max(filter(lambda range: range.src <= src, self.ranges))

    def get_dest(self, src):
        range_dst = self._range(src)
        return range_dst.get_dest(src)

    def get_splitpoints(self, src_start, src_end):
        range_start = self._range(src_start)
        range_end   = self._range(src_end)
        if range_end != range_start:
            yield range_start.get_dest(src_start), range_start.maxdest
            for r in sorted(filter(lambda r: r.src > src_start and r.src <= src_end, self.ranges)):
                if r != range_end:
                    yield r.dest, r.maxdest
                else:
                    yield r.dest, r.get_dest(src_end)
        else:
            yield range_start.get_dest(src_start), range_start.get_dest(src_end)

class AlmanacGame:

    def __init__(self):
        self.seeds = data.seeds
        self.seed_soil = Depends('seed-to-soil')
        self.soil_fertilizer = Depends('soil-to-fertilizer')
        self.fertilizer_water = Depends('fertilizer-to-water')
        self.water_light = Depends('water-to-light')
        self.light_temperature = Depends('light-to-temperature')
        self.temperature_humidity = Depends('temperature-to-humidity')
        self.humidity_location = Depends('humidity-to-location')

    def read_data(self):
        self.seed_soil.read_data(data.seed_to_soil)
        self.soil_fertilizer.read_data(data.soil_to_fertilizer)
        self.fertilizer_water.read_data(data.fertilizer_to_water)
        self.water_light.read_data(data.water_to_light)
        self.light_temperature.read_data(data.light_to_temperature)
        self.temperature_humidity.read_data(data.temperature_to_humidity)
        self.humidity_location.read_data(data.humidity_to_location)

    def get_location(self, seed):
        return self.humidity_location.get_dest(
            self.temperature_humidity.get_dest(
            self.light_temperature.get_dest(
            self.water_light.get_dest(
            self.fertilizer_water.get_dest(
            self.soil_fertilizer.get_dest(
            self.seed_soil.get_dest(seed)))))))

    def part1_min_location(self):
        loc = min(map(self.get_location, self.seeds))
        return loc

    def part2_min_location(self):
        min_location = sys.maxsize
        for i in range(0, len(data.seeds), 2):
            for soil_s, soil_e in self.seed_soil.get_splitpoints(data.seeds[i], data.seeds[i]+data.seeds[i+1]):
                for fertilizer_s, fertilizer_e in self.soil_fertilizer.get_splitpoints(soil_s, soil_e):
                    for water_s, water_e in self.fertilizer_water.get_splitpoints(fertilizer_s, fertilizer_e):
                        for light_s, light_e in self.water_light.get_splitpoints(water_s, water_e):
                            for temp_s, temp_e in self.light_temperature.get_splitpoints(light_s, light_e):
                                for humidity_s, humidity_e in self.temperature_humidity.get_splitpoints(temp_s, temp_e):
                                    for location_s, location_e in self.humidity_location.get_splitpoints(humidity_s, humidity_e):
                                        if location_s < min_location:
                                            min_location = location_s
        return min_location

def main():
    game = AlmanacGame()
    game.read_data()
    # pp.pprint(game.seed_soil.data)
    # pp.pprint(game.seed_soil)
    print(game.part1_min_location())
    print(game.part2_min_location())

if __name__ == '__main__':
    main()
