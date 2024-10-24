import numpy as np

import config

class RandomPlayer:
 def __init__(self):
  self.name="random"
  self.symbol=""
  self.opponent_symbol=""

 def choose_move(self,game):
  available_moves=[
   (row,col)
   for row in range(config.settings["game"]["n_rows"])
   for col in range(config.settings["game"]["n_cols"])
   if game.board.cells[row,col]==config.empty_cell_symbol
  ]
  return available_moves[np.random.choice(len(available_moves))]
