import numpy as np
import pickle

import config

class DataStorage:
 def __init__(self,filename='training_data.pkl'):
  self.filename=filename
  self.training_data=[]
  self.n_rows=config.settings["game"]["n_rows"]
  self.n_cols=config.settings["game"]["n_cols"]
  self.empty_cell_symbol=config.settings["game"]["empty_cell_symbol"]

 def save_game(self,game_data,winner_symbol):
  if config.settings["details"]:
   print(f"winner_symbol: {winner_symbol}")
   print()
  for data in game_data:
   if config.settings["details"]:
    print(data)
  # Process the board states that were saved during the game.
  for board_state_before_move,player_symbol,move in game_data:
   if winner_symbol=='':
    if config.settings["details"]:
     print(f"From this position this move led to draw for the {player_symbol} player.")
    game_value_for_player=config.settings["train"]["draw_value"]
   if winner_symbol==player_symbol:
    if config.settings["details"]:
     print(f"From this position this move led to win for the {player_symbol} player.")
    game_value_for_player=config.settings["train"]["win_value"]
   if winner_symbol==config.opponent(player_symbol):
    if config.settings["details"]:
     print(f"From this position this move led to loss for the {player_symbol} player.")
    game_value_for_player=config.settings["train"]["loss_value"]
   # Prepare a new input matrix.
   input=np.zeros((self.n_rows,config.settings["game"]["n_cols"]),dtype=int)
   # Prepare a new target matrix.
   target=np.zeros((self.n_rows,self.n_cols),dtype=float)
   n_free_cells_after_move=np.count_nonzero(board_state_before_move=='-')-1
   if config.settings["details"]:
    print(f"board_state_before_move: \n{board_state_before_move}")
    print(f"player_symbol: {player_symbol}")
    print(f"move: {move}")
   # Set input values.
   if config.settings["details"]:
    print(f"Input will be a matrix of the same size as the board, where")
    print(f" - for every empty cell of the board we put a 0 in the relevant input cell,")
    print(f" - for every {player_symbol} cell of the board we put a 1 in the relevant input cell, and")
    print(f" - for every {config.opponent(player_symbol)} cell of the board we put a -1 in the relevant input cell.")
   for row in range(self.n_rows):
    for col in range(self.n_cols):
     if board_state_before_move[row,col]==self.empty_cell_symbol:
      input[row,col]=0
     if board_state_before_move[row,col]==player_symbol:
      input[row,col]=1
     if board_state_before_move[row,col]==config.opponent(player_symbol):
      input[row,col]=-1
   # Set target values.
   if n_free_cells_after_move>=1:
    calculated=(1.0-game_value_for_player)/n_free_cells_after_move
   else:
    calculated=1000.0
   for row in range(self.n_rows):
    for col in range(self.n_cols):
     if (row,col)==move:
      target[row,col]=game_value_for_player
     elif board_state_before_move[row,col]==self.empty_cell_symbol:
      target[row,col]=calculated
     else:
      target[row,col]=0.0
   if config.settings["details"]:
    print(f"input: \n{input}")
   flat_input=input.flatten().tolist()
   flat_target=target.flatten().tolist()
   if config.settings["details"]:
    print(flat_input)
    print(flat_target)
   self.training_data.append((flat_input,flat_target))
    
 def save_to_file(self):
  with open(self.filename,'wb') as f:
   pickle.dump(self.training_data,f)
    
 def load_from_file(self):
  with open(self.filename,'rb') as f:
   self.training_data=pickle.load(f)
