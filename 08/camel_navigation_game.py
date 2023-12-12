import re
import sys
from IPython.core.debugger import set_trace
import math

class Crossroad:

    def __init__(self, label):
        self.id    = label[:3]
        self.left  = label[3:6]
        self.right = label[6:9]
        # part 2
        self.is_starting_node = self.id.endswith('A')
        self.is_ending_node = self.id.endswith('Z')

    def go(self, direction):
        if direction == 'L':
            return self.left
        elif direction == 'R':
            return self.right
        else:
            raise Exception(f'Direction {direction} not applicable')

    def __repr__(self):
        return f'Crossroad({self.id}: {self.left.id} {self.right.id})'


class Path:
    """part 2, notes on the trodden paths"""

    def __init__(self, crossroad, turn_id, explored_by_ghost):
        self.crossroad     = crossroad
        self.turn_id_start = turn_id
        self.ghost_id      = explored_by_ghost
        self.ending_nodes  = [] # index of the nodes with possible game end
        self.allturns_dest = None # crossroad at which we finish after one cycle of direction letters is spent

    def add_ending_turn(self, turn_id):
        self.ending_nodes.append(turn_id - self.turn_id_start)

    def __repr__(self):
        return f'Path([{self.crossroad.id}, {self.turn_id_start}, {self.ghost_id}]) => {self.allturns_dest} {self.ending_nodes}'


class CamelNavigation:

    def __init__(self, filename):
        self.turns = []
        self.crossroads = {} # id: object
        with open(filename, 'r') as f:
            self.turns = [c for c in f.readline().rstrip()]
            self.turns_cycle = len(self.turns)
            self.ghost_starts = []
            for line in f.readlines():
                line = re.sub('[^A-Z0-9]+', '', line)
                if len(line) == 9:
                    croad = Crossroad(line)
                    self.crossroads[croad.id] = croad
                    if croad.is_starting_node:
                        self.ghost_starts.append(croad)
        # replace crossroad left, right destination labels with real objects
        for croad in self.crossroads.values():
            croad.left = self.crossroads[croad.left]
            croad.right = self.crossroads[croad.right]

    def __repr__(self):
        return str(self.crossroads)

    def part1_turns_from_AAA_to_ZZZ(self):
        croad = self.crossroads['AAA']
        i = 0
        while croad.id != 'ZZZ':
            croad = croad.go(self.turns[i % self.turns_cycle])
            i += 1
        return i

    def part2_ghost_turns_DISCARDED(self):
        """presumably, brute force would take too much time.. therefore for
        each turn_cycle, we'll try to note the paths the ghosts already went.
        we can skip in turn_cycle chunks, once all the paths are explored
        """
        turn_id    = 0
        nr_ghosts  = len(self.ghost_starts)
        ghosts_pos = list(self.ghost_starts)
        trodden   = {} # here, we'll note the paths we went through, key=(crossroad, phase)
        exploring  = {} # paths being explored, key=(ghost, phase)
        do_loop = True
        while do_loop:
            phase = turn_id % self.turns_cycle
            if turn_id == 0 or len(exploring) > 0:
                direction = self.turns[phase]
                num_ghosts_on_ending_node = 0
                for ghost_id in range(nr_ghosts):
                    croad = ghosts_pos[ghost_id]
                    explorer_id = (ghost_id, phase)
                    # if this is an ending node, mark it on all exploring paths
                    if croad.is_ending_node:
                        num_ghosts_on_ending_node += 1
                        for cycle_id in range(self.turns_cycle):
                            path = exploring.get((ghost_id, cycle_id), None)
                            if path is not None:
                                path.add_ending_turn(turn_id)
                    # note the destination for the path taken one cycle before
                    path = exploring.get(explorer_id, None)
                    if path is not None:
                        path.allturns_dest = croad
                        trodden[(path.crossroad, phase)] = path
                        del exploring[explorer_id]
                    # take a look if the path in front was already taken by others
                    trodden_id = (croad, phase)
                    path = trodden.get(trodden_id, None)
                    if path is None: # no, we are the first explorer
                        path = Path(croad, turn_id, ghost_id)
                        if croad.is_ending_node:
                            print(f'Had an ending in one {croad}, turn {turn_id}')
                            path.add_ending_turn(turn_id)
                        exploring[explorer_id] = path

                if num_ghosts_on_ending_node == nr_ghosts:
                    print(f'All ghosts on ending node in {turn_id}')
                    do_loop = False
                else:
                    for ghost_id in range(nr_ghosts):
                        ghosts_pos[ghost_id] = ghosts_pos[ghost_id].go(direction)
                turn_id += 1
            else: # we can go in self.turns_cycle chunks
                # let's take a look if we have similar ending_nodes in trodden paths
                # set_trace()
                ending_nodes_cnt = {}
                for ghost_id in range(nr_ghosts):
                    for ending_node in trodden[(ghosts_pos[ghost_id], phase)].ending_nodes:
                        if ending_node not in ending_nodes_cnt:
                            ending_nodes_cnt[ending_node] = 1
                        else:
                            ending_nodes_cnt[ending_node] += 1
                if len(ending_nodes_cnt) > 0:
                    # set_trace()
                    # print(f'Possible {ending_nodes_cnt}')
                    max_nodes = max(ending_nodes_cnt.values())
                    if max_nodes > 3:
                        print(f'{max_nodes} ghosts matched ending in {turn_id}')
                    if max_nodes == nr_ghosts:
                        min_node = min([item[0] for item in ending_nodes_cnt.items() if item[1] == max_nodes])
                        print(f'Exit in {turn_id+min_node}')
                        do_loop = False
                    else:
                        for ghost_id in range(nr_ghosts):
                            ghosts_pos[ghost_id] = trodden[(ghosts_pos[ghost_id], phase)].allturns_dest
                else:
                    for ghost_id in range(nr_ghosts):
                        ghosts_pos[ghost_id] = trodden[(ghosts_pos[ghost_id], phase)].allturns_dest
                turn_id += self.turns_cycle
            if turn_id % 1000000 == 0:
                print(f'turn_id: {turn_id}, trodden: {len(trodden)}')
                # set_trace()
                # return

    def analyze(self, starting_node):
        if type(starting_node) is str:
            croad = self.crossroads[starting_node]
        else:
            croad = starting_node
        i = 0
        while not croad.is_ending_node:
            croad = croad.go(self.turns[i % self.turns_cycle])
            i += 1
        return starting_node, i, croad

    def part2_ghost_turns(self):
        """the solution was found after receiving hint to take a look at the input in
        which it was noticed that the ending crossroad of each ghost led to the second
        crossroad of the path, making it predictable without exhaustion.
        For the provided input:
        starts:
        [Crossroad(GNA: VSL QGP),
         Crossroad(FCA: QHT STM),
         Crossroad(AAA: SGB VQJ),
         Crossroad(MXA: VLS FNP),
         Crossroad(VVA: JSB DJH),
         Crossroad(XHA: HKR SBX)]
        second crossroad:
        [Crossroad(VSL: NMG LPG),
         Crossroad(QHT: BKC LHC),
         Crossroad(SGB: KQV VLM),
         Crossroad(VLS: BSG BDS),
         Crossroad(JSB: SGV FMP),
         Crossroad(HKR: VPP TCL)]
        ending nodes (notice that they lead to the second crossroad of other ghost
        [Crossroad(XDZ: STM QHT),
         Crossroad(JVZ: DJH JSB),
         Crossroad(DDZ: QGP VSL),
         Crossroad(THZ: SBX HKR),
         Crossroad(SRZ: FNP VLS),
         Crossroad(ZZZ: VQJ SGB)]
        also, number of turns in which the ghost reached end had to be divisible
        by the input turns cycle without a reminder, which was found to be true
        """
        loops = list(map(self.analyze, self.ghost_starts))
        if max(map(lambda loop: loop[1] % self.turns_cycle, loops)) > 0:
            print(f'sorry, not all ghosts will loop in predictable way due to start-end cycle length')
            print(loops)
            return None
        if any(filter(lambda loop: loop[0].right != loop[2].left, loops)):
            print(f'sorry, not all ghosts will loop in a predictable way due to the expected continuation crossroad')
            print(loops)
            return None
        # ok, find the least common multiple from found ghost cycles
        return math.lcm(*map(lambda loop: loop[1], loops))


def main(filename):
    game = CamelNavigation(filename)
    # print(game.part1_turns_from_AAA_to_ZZZ())
    print(game.part2_ghost_turns())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = 'input.txt'
    else:
        filename = sys.argv[1]
    main(filename)
