import re
import sys

class BagPick:

    def __init__(self, pickline, red=0, green=0, blue=0):
        self.pickline = pickline
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return f'"{self.pickline}"=R:{self.red} G:{self.green} B:{self.blue}'

class Game:

    def __init__(self, gameid):
        self.gameid = gameid
        self.picks = []
        self.possible = False

    def add_pick(self, pickline):
        self.picks.append(self._parse_pick(pickline))

    def _parse_pick(self, pickline):
        pick = BagPick(pickline)
        for colorpick in pickline.split(', '):
            parts = re.match('([0-9]+) (.*)', colorpick)
            if parts is None:
                continue
            parts = parts.groups()
            setattr(pick, parts[1], int(parts[0]))
        return pick

    def is_possible(self, bag_reds, bag_greens, bag_blues):
        return not any(filter(lambda pick: pick.red > bag_reds or pick.green > bag_greens or pick.blue > bag_blues,
               self.picks))

    def __repr__(self):
        return f'Game {self.gameid}: {self.picks}'

class CubeGame:

    def __init__(self, inputfile, bag_reds, bag_greens, bag_blues):
        self.bag_reds = bag_reds
        self.bag_greens = bag_greens
        self.bag_blues = bag_blues
        self.lines = open(inputfile, 'r').readlines()
        
    def part1_sum_possible_games(self):
        return sum(map(lambda g: g.gameid, self._possible_games()))

    def _possible_games(self):
        for line in self.lines:
            game = self._parse_game(line)
            if game and game.is_possible(self.bag_reds, self.bag_greens, self.bag_blues):
                yield game

    def _parse_game(self, line):
        parts = re.match('Game ([0-9]+): (.*)', line)
        if parts is None:
            return None
        parts = parts.groups()
        game = Game(int(parts[0]))
        for pickline in parts[1].split(';'):
            game.add_pick(pickline.strip())
        return game

    def part2_sum_powers(self):
        sum_powers = 0
        for line in self.lines:
            game = self._parse_game(line)
            min_reds = max(map(lambda pick: 1 if pick.red == 0 else pick.red, game.picks))
            min_greens = max(map(lambda pick: 1 if pick.green == 0 else pick.green, game.picks))
            min_blues = max(map(lambda pick: 1 if pick.blue == 0 else pick.blue, game.picks))
            gamepower = min_reds * min_greens * min_blues
            sum_powers += gamepower
        return sum_powers


def main(filename):
    game = CubeGame(filename, 12, 13, 14)
    print(game.part1_sum_possible_games())
    print(game.part2_sum_powers())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = 'input.txt'
    else:
        filename = sys.argv[1]
    main(filename)
