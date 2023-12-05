digits = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

class Calibrate:

    def __init__(self, fname, part2=False):
        self.lines = open(fname, 'r').readlines()
        self.part2 = part2

    def sum_overal(self):
        return sum(map(lambda l: self._sum_line(l), self.lines))

    def _sum_line(self, line):
        if self.part2:
            digits = [c for c in self._get_digits(line)]
        else:
            digits = [c for c in line if c.isdigit()]
        if len(digits) < 2:
            digits.append(digits[0])
        return int(digits[0] + digits[-1])

    def _get_digits(self, line):
        idx = 0
        while idx < len(line):
            if line[idx].isdigit():
                yield line[idx]
                idx += 1
            else:
                for k, v in digits.items():
                    if line[idx:].startswith(k):
                        idx += len(k) - 1 # note: eightwo needs to be read as 8, 2 even though t is also part of eight
                        yield v
                        break
                else:
                    idx += 1

def main():
    c = Calibrate('input.txt', False)
    print(c.sum_overal())

if __name__ == '__main__':
    main()
