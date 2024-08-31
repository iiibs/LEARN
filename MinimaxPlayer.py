import numpy as np

import config

class MinimaxPlayer:
 def __init__(self):
  self.symbol=""
  self.opponent_symbol=""

 def choose_move(self,game,fix_openings=True):
  if fix_openings:
   # If all cells are empty, then take the center
   if np.all(game.board.cells==config.empty_cell_symbol):
    center=(config.n_rows//2,config.n_cols//2)
    if game.board.cells[center[0],center[1]]==config.empty_cell_symbol:
     return center
   opponent_stones=[(row, col) for row in range(config.n_rows) for col in range(config.n_cols)
                    if game.board.cells[row, col]==self.opponent_symbol]
   if len(opponent_stones)==1:
    opponent_move=opponent_stones[0]
    if opponent_move==(0,0):
     return (1,1)
    elif opponent_move==(0,1):
     return (0,0)
    elif opponent_move==(0,2):
     return (1,1)
    elif opponent_move==(1,0):
     return (0,0)
    elif opponent_move==(1,1):
     return (0, 0)
    elif opponent_move==(1,2):
     return (0,2)
    elif opponent_move==(2,0):
     return (1,1)
    elif opponent_move==(2,1):
     return (0,1)
    elif opponent_move==(2,2):
     return (1,1)
  best_score=float('-inf')
  best_move=None
  for row in range(config.n_rows):
   for col in range(config.n_cols):
    if game.board.cells[row,col]==config.empty_cell_symbol:
     game.board.cells[row,col]=self.symbol
     score=self.minimax(game,0,False)
     game.board.cells[row,col]=config.empty_cell_symbol
     if score>best_score:
      best_score=score
      best_move=(row, col)
  return best_move

 def minimax(self,game,depth,is_maximizing):
  if game.is_winner(self.symbol):
   return 1
  if game.is_winner(self.opponent_symbol):
   return -1
  if game.is_draw():
   return 0
  if is_maximizing:
   best_score=float('-inf')
   for row in range(config.n_rows):
    for col in range(config.n_cols):
     if game.board.cells[row,col]==config.empty_cell_symbol:
      game.board.cells[row,col]=self.symbol
      score=self.minimax(game,depth+1,False)
      game.board.cells[row, col]=config.empty_cell_symbol
      best_score=max(score,best_score)
   return best_score
  else:
   best_score = float('inf')
   for row in range(config.n_rows):
    for col in range(config.n_cols):
     if game.board.cells[row,col]==config.empty_cell_symbol:
      game.board.cells[row,col]=self.opponent_symbol
      score=self.minimax(game,depth+1,True)
      game.board.cells[row,col]=config.empty_cell_symbol
      best_score=min(score,best_score)
   return best_score
