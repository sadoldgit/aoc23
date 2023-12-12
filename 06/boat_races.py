from functools import reduce

class Race:
    def __init__(self, time, record_distance):
        self.time = time
        self.record_distance = record_distance

    def winning_times(self):
        for hold in range(1, self.time):
            distance = hold * (self.time - hold)
            if distance > self.record_distance:
                yield distance

class BoatRaces:

    def __init__(self, records):
        self.races = [Race(k, v) for k, v in records.items()]

    def part1_num_of_ways_to_beat(self):
        return reduce(lambda a, b: a * b,
            map(lambda times: len(list(times)),
            map(lambda race: race.winning_times(), self.races)))


def main():
# note: input manually prepared from:
#Time:        41     77     70     96
#Distance:   249   1362   1127   1011
    races = BoatRaces({
    41: 249,
    77: 1362,
    70: 1127,
    96: 1011})
    print(races.part1_num_of_ways_to_beat())
    # part 2, why think of the formula when we can try with the brute force
    race = Race(41777096, 249136211271011)
    print(len(list(race.winning_times())))
    # p.s. the formula is actually quadratic equation:
    #    hold_time*(race_time-hold_time) > distance
    #    -hold_time^2 + race_time*hold_time - distance > 0

if __name__ == '__main__':
    main()
