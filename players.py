import random

import numpy as np

from board import Board


class Random(object):

    def make_next_move(self, board: Board):
        pos = random.choice(list(board.available_places[board.turn].keys()))
        board.place_disc(pos)


class Greedy(object):

    def make_next_move(self, board: Board):
        places = board.available_places[board.turn]
        pos = sorted(places, key=lambda pos: len(places[pos]), reverse=True)[0]
        board.place_disc(pos)


HEUR = [[100, -25, 10, 5, 5, 10, -25, 100],
        [-25, -25, 2, 2, 2, 2, -25, -25],
        [10, 2, 5, 1, 1, 5, 2, 10],
        [5, 2, 1, 2, 2, 1, 2, 5],
        [5, 2, 1, 2, 2, 1, 2, 5],
        [10, 2, 5, 1, 1, 5, 2, 10],
        [-25, -25, 2, 2, 2, 2, -25, -25],
        [100, -25, 10, 5, 5, 10, -25, 100]]

HEUR4X4 = [[100, -25, -25, 100],
           [-25, -25, -25, -25],
           [-25, -25, -25, -25],
           [100, -25, -25, 100]]

HEUR6X6 = [[100, -25, 10, 10, -25, 100],
           [-25, -25, 2, 2, -25, -25],
           [10, 2, 5, 5, 2, 10],
           [10, 2, 5, 5, 2, 10],
           [-25, -25, 2, 2, -25, -25],
           [100, -25, 10, 10, -25, 100]]

BENCH = [[80, -26, 24, -1, -5, 28, -18, 76],
         [-23, -39, -18, -9, -6, -8, -39, -1],
         [46, -16, 4, 1, -3, 6, -20, 52],
         [-13, -5, 2, -1, 4, 3, -12, -2],
         [-5, -6, 1, -2, -3, 0, -9, -5],
         [48, -13, 12, 5, 0, 5, -24, 41],
         [-27, -53, -11, -1, -11, -16, -58, -15],
         [87, -25, 27, -1, 5, 36, -3, 100]]


class SmartGreedy(object):

    def make_next_move(self, board: Board):
        assert board.NUM_ROWS in (4, 6, 8)

        if board.NUM_ROWS == 4:
            weight = np.array(HEUR4X4)
        elif board.NUM_ROWS == 6:
            weight = np.array(HEUR6X6)
        else:
            weight = np.array(HEUR)

        best_pos = (None, -float('inf'))
        for pos in board.available_places[board.turn]:
            dup = board.dup()
            dup.place_disc(pos)
            point = np.sum(dup.board * weight)
            if point > best_pos[1]:
                best_pos = (pos, point)
        board.place_disc(best_pos[0])


class MinMax(object):

    def min_max(self, board: Board, depth, who_am_i):

        return self._alpha_beta(
            board,
            depth,
            who_am_i,
            (None, -float('inf')),
            (None, float('inf'))
        )

    def _alpha_beta(self, board, depth, who_am_i, max_pos, min_pos):
        if depth == 0 or board.state != board.ACTIVE:
            value = board.scores[board.PLAYER_BLACK] - board.scores[board.PLAYER_WHITE]
            if who_am_i == board.PLAYER_WHITE:
                value *= -1
            return (None, value)

        if board.turn == who_am_i:
            for pos in board.available_places[board.turn]:
                dup = board.dup()
                dup.place_disc(pos)
                score = self._alpha_beta(dup, depth - 1, who_am_i, max_pos, min_pos)
                if score[1] > max_pos[1]:
                    max_pos = (pos, score[1])
                if max_pos[1] >= min_pos[1]:
                    break
            return max_pos
        else:
            for pos in board.available_places[board.turn]:
                dup = board.dup()
                dup.place_disc(pos)
                score = self._alpha_beta(dup, depth - 1, who_am_i, max_pos, min_pos)
                if score[1] < min_pos[1]:
                    min_pos = (pos, score[1])
                if max_pos[1] >= min_pos[1]:
                    break
            return min_pos

    def make_next_move(self, board: Board):
        best_pos = self.min_max(board, board.NUM_ROWS // 2, board.turn)
        board.place_disc(best_pos[0])


class NaiveMCTS(object):

    def make_next_move(self, board: Board):
        who_am_i = board.turn
        results = {}
        for _ in range(100):
            result = self.playout(board.dup(), who_am_i)
            if result[0] not in results:
                results[result[0]] = {'visited': 0, 'value': 0}
            else:
                results[result[0]]['visited'] += 1
                if result[1] == board.WON_BLACK:
                    if who_am_i == board.PLAYER_BLACK:
                        results[result[0]]['value'] += 1
                    else:
                        results[result[0]]['value'] -= 1
                elif result[1] == board.WON_WHITE:
                    if who_am_i == board.PLAYER_WHITE:
                        results[result[0]]['value'] += 1
                    else:
                        results[result[0]]['value'] -= 1

        best_pos = sorted(results,
                          key=lambda x: results[x]['value'] / results[x]['visited'],
                          reverse=True)[0]
        board.place_disc(best_pos)

    def playout(self, board: Board, who_am_i):
        selected = None
        while board.state == board.ACTIVE:
            pos = random.choice(list(board.available_places[board.turn].keys()))
            board.place_disc(pos)
            if selected is None:
                selected = pos
        return (selected, board.state)
