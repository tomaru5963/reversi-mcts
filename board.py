import numpy as np


class Board(object):
    NUM_ROWS = 4
    NUM_COLS = 4

    ACTIVE = 0
    DRAW = 1
    WON_BLACK = 2
    WON_WHITE = 3

    EMPTY = 0
    PLAYER_BLACK = 1
    PLAYER_WHITE = -1

    def __init__(self):
        self.board = np.zeros((self.NUM_ROWS, self.NUM_COLS), np.int32)
        self.board[self.NUM_ROWS // 2, self.NUM_COLS // 2 - 1] = self.PLAYER_BLACK
        self.board[self.NUM_ROWS // 2 - 1, self.NUM_COLS // 2] = self.PLAYER_BLACK
        self.board[self.NUM_ROWS // 2 - 1, self.NUM_COLS // 2 - 1] = self.PLAYER_WHITE
        self.board[self.NUM_ROWS // 2, self.NUM_COLS // 2] = self.PLAYER_WHITE

        self.state = self.ACTIVE
        self.turn = self.PLAYER_BLACK
        self.scores = {self.PLAYER_BLACK: 2, self.PLAYER_WHITE: 2}
        self.available_places = {self.PLAYER_BLACK: {}, self.PLAYER_WHITE: {}}
        self.update_state()

    def dup(self):
        new = Board()
        new.board = self.board.copy()
        new.state = self.state
        new.turn = self.turn
        new.scores = self.scores.copy()
        new.available_places = self.available_places.copy()
        return new

    def update_state(self):
        self.scores[self.PLAYER_BLACK] = np.sum(self.board == self.PLAYER_BLACK)
        self.scores[self.PLAYER_WHITE] = np.sum(self.board == self.PLAYER_WHITE)

        self.available_places[self.PLAYER_BLACK] = {}
        self.available_places[self.PLAYER_WHITE] = {}
        empties = np.where(self.board == self.EMPTY)
        for empty_pos in zip(empties[0], empties[1]):
            for player in (self.PLAYER_BLACK, self.PLAYER_WHITE):
                turnables = self.get_turnables(empty_pos, player)
                if turnables:
                    self.available_places[player][empty_pos] = turnables

        if (self.available_places[self.PLAYER_BLACK] or
                self.available_places[self.PLAYER_WHITE]):
            self.state = self.ACTIVE
        elif self.scores[self.PLAYER_BLACK] == self.scores[self.PLAYER_WHITE]:
            self.state = self.DRAW
        elif self.scores[self.PLAYER_BLACK] > self.scores[self.PLAYER_WHITE]:
            self.state = self.WON_BLACK
        else:
            self.state = self.WON_WHITE

    def get_turnables(self, pos, player):
        def turnables_for_line(direction):
            row = pos[0] + direction[0]
            col = pos[1] + direction[1]
            cells = []
            while 0 <= row < self.NUM_COLS and 0 <= col < self.NUM_COLS:
                if self.board[row, col] == self.EMPTY:
                    break
                if self.board[row, col] == player:
                    return cells
                cells.append((row, col))
                row += direction[0]
                col += direction[1]
            return []

        turnables = []
        for direction in ((-1, -1), (-1, 0), (-1, 1),
                          (0, -1), (0, 1),
                          (1, -1), (1, 0), (1, 1)):
            turnables.extend(turnables_for_line(direction))
        return turnables

    def place_disc(self, pos):
        assert self.state == self.ACTIVE
        assert pos in self.available_places[self.turn].keys()

        self.board[pos] = self.turn
        rows, cols = zip(*self.available_places[self.turn][pos])
        self.board[rows, cols] = self.turn

        self.update_state()
        if self.state == self.ACTIVE:
            if (self.turn == self.PLAYER_BLACK and
                    len(self.available_places[self.PLAYER_WHITE]) > 0):
                self.turn = self.PLAYER_WHITE
            elif (self.turn == self.PLAYER_WHITE and
                  len(self.available_places[self.PLAYER_BLACK]) > 0):
                self.turn = self.PLAYER_BLACK


def play_game(black, white):
    board = Board()
    players = {board.PLAYER_BLACK: black, board.PLAYER_WHITE: white}

    while board.state == board.ACTIVE:
        players[board.turn].make_next_move(board)

    return board.state
