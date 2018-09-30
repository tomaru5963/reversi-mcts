import itertools

import numpy as np

from board import Board, play_game
from players import Random, Greedy, MinMax, NaiveMCTS


def main():

    # players = [Random, Greedy, SmartGreedy, MinMax, NaiveMCTS]
    players = [Random, Greedy, MinMax, NaiveMCTS]
    num_players = len(players)
    head2head = np.zeros((num_players, num_players))

    NUM_SESSIONS = 100
    for player1, player2 in itertools.combinations(enumerate(players), 2):
        for session in range(NUM_SESSIONS):
            for black, white in ((player1, player2), (player2, player1)):
                result = play_game(black[1](), white[1]())
                if result == Board.WON_BLACK:
                    head2head[black[0], white[0]] += 1
                elif result == Board.WON_WHITE:
                    head2head[white[0], black[0]] += 1
        print(player1, player2)
        print(head2head / (NUM_SESSIONS * 2))

    print(list(enumerate(players)))
    print(head2head / (NUM_SESSIONS * 2))


if __name__ == '__main__':
    main()
