import numpy as np

import config

class HumanPlayer:
 def __init__(self):
  self.symbol = ""
  self.opponent_symbol = ""

 def choose_move(self, game):
  if config.settings["game"]["name"]=="tic-tac-toe":
   valid_moves = {
    'a1': (2, 0), 'a2': (1, 0), 'a3': (0, 0),
    'b1': (2, 1), 'b2': (1, 1), 'b3': (0, 1),
    'c1': (2, 2), 'c2': (1, 2), 'c3': (0, 2)
   }
  if config.settings["game"]["name"]=="OXXO":
   valid_moves={'a1':(0,0),'b1':(0,1),'c1':(0,2),'d1':(0,3),}
  while True:
   move = input("Enter your move using chessboard notation: ").strip().lower()
   if move in valid_moves:
    row, col = valid_moves[move]
    if game.board.cells[row, col]==config.settings["game"]["empty_cell_symbol"]:
     return (row, col)
    else:
     print("Invalid move: Cell is already occupied.")
   else:
    print("Invalid move: Please enter a valid move (e.g., a1, b2, c3).")

