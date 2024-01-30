import sys

class History:

    def __init__(self, line):
        self.history = [int(val) for val in line.split(' ')]
        self.diffs = []
        diff = self._history_diffs(self.history)
        while any(diff):
            self.diffs.append(diff)
            diff = self._history_diffs(diff)
        self.diffs.append(diff) # append zeros
        self.prediction = self.history[-1] # all equal already
        if any(self.diffs):
            self.prediction += self._predict()
        #second part
        self.prediction_left = self.history[0] # all equal already
        if any(self.diffs):
            self.prediction_left -= self._predict_left()

    def _history_diffs(self, history):
        return [history[i] - history[i-1] for  i in range(1, len(history))]

    def _predict(self, diffidx=0):
        diff = self.diffs[diffidx]
        if diffidx < len(self.diffs) - 1:
            return diff[-1] + self._predict(diffidx + 1)
        else:
            return 0

    # second part
    def _predict_left(self, diffidx=0):
        diff = self.diffs[diffidx]
        if diffidx < len(self.diffs) - 1:
            return diff[0] - self._predict_left(diffidx + 1)
        else:
            return 0

    def __repr__(self):
        diffs = '\n'.join([str(d) for d in self.diffs])
        return str(self.history) + '\nprediction:' + str(self.prediction) + '\n' + diffs + '\n'

class MirageMaintenance:

    def __init__(self, filename):
        self.histories = []
        with open(filename, 'r') as f:
            for line in f.readlines():
                history = History(line.rstrip())
                self.histories.append(history)

    def __repr__(self):
        return str(self.histories)

    def part1_prediction(self):
        return sum(map(lambda h: h.prediction, self.histories))

    def part1_prediction_left(self):
        return sum(map(lambda h: h.prediction_left, self.histories))

def main(filename):
    game = MirageMaintenance(filename)
    # print(game)
    print(game.part1_prediction())
    print(game.part1_prediction_left())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = 'input.txt'
    else:
        filename = sys.argv[1]
    main(filename)
