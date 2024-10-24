import numpy as np
import pickle
import os
import time
from datetime import datetime
import threading

import config
from PerfectPlayer import *
from RandomPlayer import *
from Game import *

class Simulate:
 def __init__(self,filename='training_data.pkl'):
  self.filename=filename
  self.training_data=[]
  self.n_rows=config.settings["game"]["n_rows"]
  self.n_cols=config.settings["game"]["n_cols"]
  self.empty_cell_symbol=config.empty_cell_symbol
  self.n_games=config.settings["simulate"]["n_games"]
  self.n_games_saved=config.settings["simulate"]["n_games_saved"]
  self.save_interval_seconds=config.settings["simulate"]["save_interval_seconds"]
  self.should_continue=True
  self.should_save=False

 def interrupt_and_set_save(self):
  while self.should_continue:
   time.sleep(self.save_interval_seconds)
   self.should_save=True

 def run(self,mode):
  file_path=self.filename

  # Start a new simulation.
  if mode=="new":
   if os.path.exists(file_path):
    os.remove(file_path)
    print(f"Simulation data {file_path} deleted.")
   else:
    print(f"Simulation data {file_path} did not exist.")

  # Continue an earlier saved simulation.
  if mode=="continue":
   if os.path.exists(file_path):
    self.load_training_data_from_file()
    print(f"Simulation data {file_path} loaded.")
    print(f"{self.n_games_saved} games already saved.")

  interrupt_thread=threading.Thread(target=self.interrupt_and_set_save)
  while self.should_continue==True:
   interrupt_thread.start()
   # Perform simulation of games and store them.
   self.store_games()
   interrupt_thread.join()

  if config.settings["details"]:
   self.print_training_data()

  # Save the simulated training data and the settings.
  self.save_training_data_to_file()
  return

 def store_games(self):
  # Perform and save games for creating training data.
  perfect_player=PerfectPlayer()
  random_player=RandomPlayer()
  for _ in range(self.n_games_saved+1,self.n_games):
   if self.should_save:
    self.save_training_data_to_file()
    self.should_continue=True
   else:
    if config.settings["game"]["name"]=="tic-tac-toe":
     game=TictactoeGame(perfect_player,random_player)
    if config.settings["game"]["name"]=="OXXO":
     game=OxxoGame(perfect_player,random_player)
    game.winner_symbol=""
    game_data=game.play()
    self.store_game(game_data,game.winner_symbol)
    self.n_games_saved+=1
    if config.settings["details"]:
     self.print_training_data
  self.save_training_data_to_file()
  self.should_continue=False

 def store_game(self,game_data,winner_symbol):
  if config.settings["details"]:
   print(f"winner_symbol: {winner_symbol}")
   print()
  if config.settings["details"]:
   self.print_training_data
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
    
 def save_training_data_to_file(self):
  # Save the simulated training data.
  with open(self.filename,'wb') as f:
   pickle.dump(self.training_data,f)
  # Save the settings.
  config.settings["simulate"]["n_games_saved"]=self.n_games_saved
  config.save_settings()
  current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  print(f"n_games_saved/n_games: {self.n_games_saved}/{self.n_games}, time: {current_time}")
  self.should_save=False
    
 def load_training_data_from_file(self):
  with open(self.filename,'rb') as f:
   self.training_data=pickle.load(f)
  config.load_settings()
  return

 def print_training_data(self):
  for i_training_data_item,(flat_input,flat_target) in enumerate(self.training_data):
   print(f"Training data item {i_training_data_item + 1}:")
   input_board=np.array(flat_input).reshape((self.n_rows,self.n_cols))
   target_matrix=np.array(flat_target).reshape((self.n_rows,self.n_cols))
   print("Input, board state before move:")
   print(input_board)
   print("Target, expected outcome for the move:")
   print(target_matrix)
   print("-" * 30)
