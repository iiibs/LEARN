import torch

import config
from PerfectPlayer import *
from RandomPlayer import *
from NeuralPlayer import *
from HumanPlayer import *
from MinimaxPlayer import *
from Game import *
from DataStorage import *
from NeuralNetwork import *

class Train:
 def __init__(self):
  self.n_games=config.settings["train"]["n_games"]
  self.n_neurons=config.settings["train"]["n_neurons"]
  self.max_points=0

 def print_game_data(self):
  for i,(input,target) in enumerate(self.storage.training_data):
   print(input)
   print(target)

 def run_old(self):
  max_z=config.settings["train"]["f"]["max_z"]
  print(f"trying to teach a neural network to earn more than {max_z} points")
  if config.settings["details"]:
   print(f"Number of games in train data: {self.n_games}")
   print(f"Number of neurons in network: {self.n_neurons}")
  # Simulate and save games, or just load the saved data.
  self.storage=DataStorage()
  if config.b_new_train_data:
   # Simulate and save games.
   perfect_player=PerfectPlayer()
   random_player=RandomPlayer()
   for _ in range(self.n_games):
    game=Game(perfect_player,random_player)
    game.winner_symbol=""
    game_data=game.play()
    self.storage.save_game(game_data,game.winner_symbol)
   # Save game data.
   self.storage.save_to_file()
   if config.settings["details"]:
    print(f'Game data stored to {self.storage.filename}')
  # Load the saved data.
  self.storage.load_from_file()
  if config.settings["details"]:
   print(f'Game data loaded from {self.storage.filename}')
   self.print_game_data()
  # Train neural network and save it, or just load the saved network
  if config.b_new_train:
   # Train neural network.
   data=self.storage.training_data
   model=NeuralNetwork()
   trained_model=train_model(model,data)
   # Save the trained neural network model.
   torch.save(trained_model.state_dict(),model.filename)
   if config.settings["details"]:
    print(f'Model saved to {model.filename}')
  # Load the saved neural network.
  model=NeuralNetwork()
  model.load_state_dict(torch.load(model.filename))
  model.eval()
  if config.settings["details"]:
   print(f'Model loaded from {model.filename}')
  # Evaluate the loaded model
  results=evaluate_model(model,config.settings["train"]["n_eval_games"])
  wins=results["wins"]
  draws=results["draws"]
  losses=results["losses"]
  config.settings["gradient"]["f"]["z"]= \
   wins*config.settings["train"]["win_value"]+ \
   draws*config.settings["train"]["draw_value"]+ \
   losses*config.settings["train"]["loss_value"]
  if config.settings["gradient"]["f"]["z"]>config.settings["gradient"]["f"]["max_z"]:
   config.settings["gradient"]["f"]["max_z"]=config.settings["gradient"]["f"]["z"]
   # Save the best neural network model.
   torch.save(trained_model.state_dict(),model.best_filename)
   print(f'Best model saved to {model.best_filename}')

 def run(self):
  if config.settings["details"]:
   print(f"Number of games in train data: {self.n_games}")
   print(f"Number of neurons in network: {self.n_neurons}")
  # Simulate and save games, or just load the saved data.
  self.storage=DataStorage()
  # Perform and save games for creating training data.
  perfect_player=PerfectPlayer()
  random_player=RandomPlayer()
  for _ in range(self.n_games):
   if config.settings["game"]["name"]=="tic-tac-toe":
    game=TictactoeGame(perfect_player,random_player)
   if config.settings["game"]["name"]=="OXXO":
    game=OxxoGame(perfect_player,random_player)
   game.winner_symbol=""
   game_data=game.play()
   self.storage.save_game(game_data,game.winner_symbol)
  # Save game data.
  self.storage.save_to_file()
  if config.settings["details"]:
   print(f'Game data stored to {self.storage.filename}')
  # Load the saved data.
  self.storage.load_from_file()
  if config.settings["details"]:
   print(f'Game data loaded from {self.storage.filename}')
   self.print_game_data()
  # Train neural network and save it, or just load the saved network
  if config.settings["train"]["new"]:
   # Train neural network.
   data=self.storage.training_data
   model=NeuralNetwork()
   trained_model=train_model(model,data)
   # Save the trained neural network model.
   torch.save(trained_model.state_dict(),model.filename)
   if config.settings["details"]:
    print(f'Model saved to {model.filename}')
  # Load the saved neural network.
  model=NeuralNetwork()
  model.load_state_dict(torch.load(model.filename))
