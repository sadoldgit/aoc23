import re
import sys
import pprint

class Card:

    LABELS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

    def __init__(self, label, value=0):
        self.label = label
        self.value = value

    @staticmethod
    def get_card(label):
        if label == '2':
            return Card(label, 2)
        elif label == '3':
            return Card(label, 3)
        elif label == '4':
            return Card(label, 4)
        elif label == '5':
            return Card(label, 5)
        elif label == '6':
            return Card(label, 6)
        elif label == '7':
            return Card(label, 7)
        elif label == '8':
            return Card(label, 8)
        elif label == '9':
            return Card(label, 9)
        elif label == 'T':
            return Card(label, 10)
        elif label == 'J':
            return Card(label, 11)
        elif label == 'Q':
            return Card(label, 12)
        elif label == 'K':
            return Card(label, 13)
        elif label == 'A':
            return Card(label, 14)

    def __gt__(self, other):
        return self.value > other.value

    def __repr__(self):
        return self.label

class Hand:

    def __init__(self, labels):
        self.labels = labels
        self.hand = []
        self.value = 0
        self.numcards = dict((k, 0) for k in Card.LABELS)
        for label in self.labels:
            card = Card.get_card(label)
            self.hand.append(card)
            self.numcards[label] += 1
        allvals = self.numcards.values()
        if 5 in allvals: # five of a kind
            self.value = 7
        elif 4 in allvals:
            self.value = 6
        elif 3 in allvals and 2 in allvals:
            self.value = 5
        elif 3 in allvals:
            self.value = 4
        elif sum([1 for num in allvals if num == 2]) == 2:
            self.value = 3
        elif 2 in allvals:
            self.value = 2
        elif sum([1 for num in allvals if num == 1]) == 5:
            self.value = 1

    def __repr__(self):
        return f'{str(self.hand)}={self.value}'

    def __gt__(self, other):
        if self.value > other.value:
            return True
        elif self.value < other.value:
            return False
        else:
            for i in range(5):
                if self.hand[i] > other.hand[i]:
                    return True
                elif self.hand[i] < other.hand[i]:
                    return False
        return False

class CamelPoker:

    def __init__(self, filename):
        self.game = {}
        for line in open(filename, 'r').readlines():
            if len(line.rstrip()) > 6:
                bid, hand = self._parse_hand(line.rstrip())
                self.game[hand] = int(bid)

    def _parse_hand(self, line):
        labels, bid = line.split(' ')
        return bid, Hand(labels)

    def _rank(self):
        return [h for h in sorted(self.game.keys())]

    def part1_total_winning(self):
        win = 0
        i = 1
        for hand in self._rank():
            win += self.game[hand] * i
            i += 1
        return win

    def __repr__(self):
        return str(self.game)

def main(filename):
    game = CamelPoker(filename)
    pprint.pprint(game._rank())
    print(game.part1_total_winning())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = 'input.txt'
    else:
        filename = sys.argv[1]
    main(filename)
