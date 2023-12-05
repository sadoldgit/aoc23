import re
import sys

class Game:

    def __init__(self, cardsid):
        self.cardsid = cardsid

    def add_cards(self, winning, my):
        self.winning = winning
        self.my = my

    def matches(self):
        missed = set(self.winning) - set(self.my)
        return len(self.winning) - len(missed)

    def winpoints(self):
        win_cards = self.matches()
        if win_cards == 0:
            return 0
        else:
            return 2 ** (win_cards - 1)

    def __repr__(self):
        return f'{self.winning} {self.my}'

class ScratchCardGame:

    def __init__(self, filename):
        self.lines = [line.rstrip() for line in open(filename, 'r').readlines()]

    def _parse_game(self, line):
        parts = re.match('Card\s+([0-9]+): (.*)', line)
        if parts is None:
            return None
        parts = parts.groups()
        game = Game(int(parts[0]))
        winning, my = parts[1].split('|')
        winning = [int(card) for card in winning.split(' ') if card.strip() != '']
        my = [int(card) for card in my.split(' ') if card.strip() != '']
        game.add_cards(winning, my)
        return game

    def part1_sum_winning(self):
        return sum(map(lambda game: game.winpoints(),
                       map(lambda line: self._parse_game(line), self.lines)))

    def part2_copy_cards(self):
        additional_cards = {}
        for line in self.lines:
            game = self._parse_game(line)
            matches = game.matches()
            # this card and previously copied cards get number of copies
            nr_cards = 1 + additional_cards.get(game.cardsid, 0)
            if matches > 0:
                for i in range(game.cardsid + 1, game.cardsid + matches + 1):
                    if i in additional_cards:
                        additional_cards[i] += nr_cards
                    else:
                        additional_cards[i] = nr_cards
        return len(self.lines) + sum([v for k, v in additional_cards.items() if k <= len(self.lines)])


def main(filename):
    cards = ScratchCardGame(filename)
    print(cards.part1_sum_winning())
    print(cards.part2_copy_cards())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = 'input.txt'
    else:
        filename = sys.argv[1]
    main(filename)
