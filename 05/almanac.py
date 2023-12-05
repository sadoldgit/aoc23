import re
import sys
# warn: input data has to be manually prepared:
import data
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Range:

    def __init__(self, dest, span):
        self.dest = dest
        self.span = span

    def __repr__(self):
        return f'->{self.dest}/{self.span}'

class Depends:

    def __init__(self, name):
        self.name = name
        self.data = None
        self.ranges = {}

    def read_data(self, maplist):
        """input data in the format [[dest1, src1, span1], [dest2, src2, span2],..]"""
        self.data = sorted(maplist, key=lambda row: row[1])
        # no definition for range 0-
        if self.data[0][1] != 0:
            self.ranges[0] = Range(0, self.data[0][1])
        rows = len(self.data)
        for i in range(0, rows):
            dst, src, span = self.data[i]
            self.ranges[src] = Range(dst, span)
            if i == rows - 1:
                continue
            _, srcnext, _ = self.data[i+1]
            if src + span < srcnext:
                newsrc = src + span
                self.ranges[newsrc] = Range(newsrc, srcnext - newsrc)

    def __repr__(self):
        return str(self.ranges)

    def find_dest(self, src):
        key = max(filter(lambda key: key < src, self.ranges.keys()))
        return self.ranges[key].dest + (src - key)

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

    def part1_min_location(self):
        loc = min(
            map(lambda src: self.humidity_location.find_dest(src),
            map(lambda src: self.temperature_humidity.find_dest(src),
            map(lambda src: self.light_temperature.find_dest(src),
            map(lambda src: self.water_light.find_dest(src),
            map(lambda src: self.fertilizer_water.find_dest(src),
            map(lambda src: self.soil_fertilizer.find_dest(src),
            map(lambda src: self.seed_soil.find_dest(src),
            self.seeds))))))))
        return loc

def main():
    game = AlmanacGame()
    game.read_data()
    # pp.pprint(game.seed_soil.data)
    # pp.pprint(game.seed_soil)
    print(game.part1_min_location())


if __name__ == '__main__':
    main()
