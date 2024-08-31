import numpy as np

import config

class Board:
 def __init__(self,n_rows,n_cols):
  self.n_rows=n_rows
  self.n_cols=n_cols
  self.empty_cell_symbol=config.settings["game"]["empty_cell_symbol"]
  self.reset()

 def reset(self):
  self.cells=np.full((self.n_rows,self.n_cols),self.empty_cell_symbol,dtype=str)

 def opposite(self,symbol):
  if symbol=="X":
   return "O"
  if symbol=="O":
   return "X"

 def copy(self):
  new_board=Board(self.n_rows, self.n_cols)
  new_board.cells=np.copy(self.cells)
  return new_board