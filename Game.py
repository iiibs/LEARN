import numpy as np
import copy

import config
from Board import *

class Game:
 def __init__(self,player1,player2):
  self.n_rows=config.settings["game"]["n_rows"]
  self.n_cols=config.settings["game"]["n_cols"]
  self.empty_cell_symbol=config.settings["game"]["empty_cell_symbol"]
  self.board=Board(self.n_rows,self.n_cols)
  self.reset(player1,player2)

 def reset(self,player1,player2):
  # Randomly decide which player starts
  choice=np.random.choice([1,-1])
  if choice==1:
   self.first_player=player1
   self.second_player=player2
  if choice==-1:
   self.first_player=player2
   self.second_player=player1
  self.current_player=self.first_player
  self.current_player.symbol='X'
  self.current_player.opponent_symbol='O'
  self.next_player=self.second_player
  self.next_player.symbol='O'
  self.next_player.opponent_symbol='X'
  self.winner_symbol=''
  self.board.reset()

 def make_move(self,row,col):
  if self.board.cells[row,col]==self.empty_cell_symbol:
   self.board.cells[row,col]=self.current_player.symbol
   return True
  return False

 def put_symbol_at(self,symbol,row,col):
  self.board.cells[row,col]=symbol

 def is_winner(self,symbol):
  raise NotImplementedError("This method should be overridden by subclasses")

 def is_draw(self):
  return np.all(self.board.cells!=self.empty_cell_symbol)

 def is_game_over(self):
  if self.is_winner('X'):
   self.winner_symbol="X"
   return_value=True
  elif self.is_winner('O'):
   self.winner_symbol="O"
   return_value=True
  elif self.is_draw():
   self.winner_symbol=""
   return_value=True
  else:
   return_value=False
  return return_value

 def get_board_as_input(self):
  if config.settings["details"]:
   print(self.board.cells)
   print(self.current_player.symbol)
  input=np.zeros((self.n_rows,self.n_cols),dtype=int)
  for row in range(self.n_rows):
   for col in range(self.n_cols):
    if self.board.cells[row,col]==self.empty_cell_symbol:
     input[row,col]=0
    if self.board.cells[row,col]==self.current_player.symbol:
     input[row,col]=1
    if self.board.cells[row,col]==config.opponent(self.current_player.symbol):
     input[row,col]=-1
  if config.settings["details"]:
   print(input)
  return input.flatten()

 def get_opponents_opening_move(self,symbol):
  # Get all the moves made by the opponent
  moves=[]
  for row in range(self.n_rows):
   for col in range(self.n_cols):
    if self.board.cells[row,col]==symbol:
     return (row,col)
    1

 def print_board(self):
  for row in self.board.cells:
   print(" ".join(cell for cell in row))
  print()

 def play(self):
  game_data=[]
  if config.settings["details"]:
   print(f"first player: {self.first_player}")
   print(f"second player: {self.second_player}")
  self.current_player=self.first_player
  if config.settings["details"]:
   self.print_board()
  while not self.is_game_over():
   if config.settings["details"]:
    print(f"symbol to move: {self.current_player.symbol}")
    print(f"player to move: {self.current_player}")
   move=self.current_player.choose_move(self)
   if config.settings["details"]:
    print(f"move: {move}")
   game_data.append((copy.deepcopy(self.board.cells),self.current_player.symbol,move))
   self.make_move(*move)
   if config.settings["details"]:
    self.print_board()
   if self.current_player==self.first_player:
    self.current_player=self.second_player
   elif self.current_player==self.second_player:
    self.current_player=self.first_player
  return game_data

class TictactoeGame(Game):
 def is_winner(self,symbol):
  # three symbols in a column
  for i in range(self.board.n_cols):
   if(self.board.cells[i,0]==symbol and
    self.board.cells[i,1]==symbol and
    self.board.cells[i,2]==symbol):
    return True
  # three symbols in a row
  for i in range(self.board.n_rows):
   if(self.board.cells[0,i]==symbol and
    self.board.cells[1,i]==symbol and
    self.board.cells[2,i]==symbol):
    return True
  # three symbols in the main diagonal
  if(self.board.cells[0,0]==symbol and
   self.board.cells[1,1]==symbol and
   self.board.cells[2,2]==symbol):
   return True
  # three symbols in the secondary diagonal
  if(self.board.cells[0,2]==symbol and
   self.board.cells[1,1]==symbol and
   self.board.cells[2,0]==symbol):
   return True
  return False

class OxxoGame(Game):
 def is_winner(self,symbol):
  # two adjacent symbols
  for col in range(self.board.n_cols-1):
   if self.board.cells[0,col]==symbol and self.board.cells[0,col+1]==symbol:
    return True
  return False