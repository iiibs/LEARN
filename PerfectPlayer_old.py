import numpy as np
import config
import random

class PerfectPlayer:
    def __init__(self):
        self.symbol = ""
        self.opponent_symbol = ""

    def choose_move(self, game):
        # Serial numbers for positions on the board
        sn = {
            "b2": (1, 1), "a3": (0, 0), "b3": (0, 1), "c3": (0, 2),
            "c2": (1, 2), "c1": (2, 2), "b1": (2, 1), "a1": (2, 0), "a2": (1, 0)
        }
        sn_list = ["b2", "a3", "b3", "c3", "c2", "c1", "b1", "a1", "a2"]

        # Store possible moves.
        possible_moves=[]
        
        # Check for a winning move
        for row in range(config.n_rows):
            for col in range(config.n_cols):
                if game.board.cells[row, col] == config.empty_cell_symbol:
                    game.board.cells[row, col] = self.symbol
                    if game.is_winner(self.symbol):
                        game.board.cells[row, col] = config.empty_cell_symbol
                        possible_moves.append((row, col))
                    game.board.cells[row, col] = config.empty_cell_symbol
        # If any winning move is found, choose randomly among them
        if possible_moves:
            return random.choice(possible_moves)
        else:
            possible_moves=[]

        # Check for a blocking move
        for row in range(config.n_rows):
            for col in range(config.n_cols):
                if game.board.cells[row, col] == config.empty_cell_symbol:
                    game.board.cells[row, col] = self.opponent_symbol
                    if game.is_winner(self.opponent_symbol):
                        game.board.cells[row, col] = config.empty_cell_symbol
                        possible_moves.append((row, col))
                    game.board.cells[row, col] = config.empty_cell_symbol
        # If any blocking move is found, choose randomly among them
        if possible_moves:
            return random.choice(possible_moves)
        else:
            possible_moves=[]

        # Default to any available move
        for row in range(config.n_rows):
            for col in range(config.n_cols):
                if game.board.cells[row, col] == config.empty_cell_symbol:
                    possible_moves.append((row, col))

        # Choose a random move among the remaining available moves
        return random.choice(possible_moves) if possible_moves else None
