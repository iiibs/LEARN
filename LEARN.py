import numpy as np
from datetime import datetime

import config
from Train import *
from PerfectPlayer import *
from NeuralPlayer import *
from NeuralNetwork import *
from HumanPlayer import *
from Evaluate import *
from Optimize import *

config.set_repeatable_random(False) # True False
config.b_details=False

def simulate_menu():
 menu_labels={
  1:"Start new simulation",
  2:"Continue earlier saved simulation",
 }
 menu_actions={
  1:lambda: simulate_games("new"),
  2:lambda: simulate_games("continue"),
 }
 while True:
  print("Simulation:")
  for i_menu in menu_labels:
   print(f"{i_menu}. {menu_labels[i_menu]}")
  choice=input("Enter your choice, or 0 to return: ")
  if choice=="0":
   break
  action=menu_actions.get(int(choice))
  action()
 return

def simulate_games(mode):
 current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 print(f"Simulation started at: {current_time}")
 simulate=Simulate()
 print(f" with n_games= {simulate.n_games}")
 simulate.run(mode)
 current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 print(f"Simulation ended at: {current_time}")
 print(f" with n_training_data_items= {len(simulate.training_data)}")
 return

def train_menu():
 menu_labels={
  1:"Start new training",
  2:"Continue earlier saved training",
 }
 menu_actions={
  1:lambda: train_neural_network("new"),
  2:lambda: train_neural_network("continue"),
 }
 while True:
  print("Training:")
  for i_menu in menu_labels:
   print(f"{i_menu}. {menu_labels[i_menu]}")
  choice=input("Enter your choice, or 0 to return: ")
  if choice=="0":
   break
  action=menu_actions.get(int(choice))
  action()
 return

def train_neural_network(mode):
 current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 print(f"Training started at: {current_time}")
 train=Train()
 print(f" with n_neurons= {train.n_neurons}")
 train.run(mode)
 current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 print(f"Training ended at: {current_time}")
 print(f" with n_neurons= {train.n_neurons}")
 return

def evaluate_neural_network():
 model=NeuralNetwork()
 evaluate=Evaluate(model)
 #config.settings["details"]=True
 b_evaluation=evaluate.run()
 #config.settings["details"]=False
 if b_evaluation:
  print(f"Evaluation result: Success.")
 else:
  print(f"Evaluation result: Fail.")
 return

def optimize_neural_network():
 optimize=Optimize()
 current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 print(f'Optimization started at: {current_time}')
 print( \
  f" with min_games= {config.settings['optimize']['min_games']}"+ \
  f", max_games= {config.settings['optimize']['max_games']}"+ \
  f", min_neurons= {config.settings['optimize']['min_neurons']}"+ \
  f", max_neurons= {config.settings['optimize']['max_neurons']}")
 b_success,optimal_games,optimal_neurons=optimize.run()
 current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 print(f'Optimization ended at: {current_time}')
 if b_success:
  print("At least one successful train was performed.")
  print(f" and the optimum is n_games: {optimal_games}, n_neurons: {optimal_neurons}")
  gameid=config.settings["gameid"]
  config.setting[gameid]["train_games"]=optimal_games
  config.setting[gameid]["train_neurons"]=optimal_neurons
  train=Train()
  train.run()
 else:
  print("No successful train was performed.")

def test_neural_network():
 human_player=HumanPlayer()
 model=NeuralNetwork()
 neural_player=NeuralPlayer(model)
 neural_player.model.load_state_dict(torch.load(model.filename))
 # Print the weights
 if config.b_details==True:
  for name,param in neural_player.model.named_parameters():
   if param.requires_grad:
    print(f"Layer: {name}")
    print(param.data)
 if config.settings["game"]["name"]=="tic-tac-toe":
  game=TictactoeGame(human_player,neural_player)
 if config.settings["game"]["name"]=="OXXO":
  game=OxxoGame(human_player,neural_player)
 game.winner_symbol=""
 b_details_save=config.settings["details"]
 config.settings["details"]=True
 game_data=game.play()
 if game.winner_symbol=='':
  print("draw")
 elif game.winner_symbol=='X':
  print(f"{game.first_player} won.")
 elif game.winner_symbol=='O':
  print(f"{game.second_player} won.")
 config.settings["details"]=b_details_save
 return

def test_perfect_player():
 human_player=HumanPlayer()
 perfect_player=PerfectPlayer()
 if config.settings["game"]["name"]=="tic-tac-toe":
  game=TictactoeGame(human_player,perfect_player)
 if config.settings["game"]["name"]=="OXXO":
  game=OxxoGame(human_player,perfect_player)
 game.winner_symbol=""
 game_data=game.play()
 if game.winner_symbol=='':
  print("draw")
 elif game.winner_symbol=='X':
  print(f"{game.first_player} won.")
 elif game.winner_symbol=='O':
  print(f"{game.second_player} won.")
 return

def choose_game():
 menu_labels={
  1:"Tic-tac-toe",
  2:"OXXO",
 }
 menu_actions={
  1:lambda:set_game(1),
  2:lambda:set_game(2),
 }
 while True:
  print("Game:")
  for i_menu in menu_labels:
   print(f"{i_menu}. {menu_labels[i_menu]}")
  choice=input("Enter your choice, or 0 to return: ")
  if choice=="0":
   break
  action=menu_actions.get(int(choice))
  action()

def set_n_games():
 print(f"n_games={config.settings['train']['n_games']}")
 value=input("Enter the new value: ")
 config.settings["train"]["n_games"]=int(value)
 print(f" n_games set to {config.settings['train']['n_games']}")

def set_n_neurons():
 print(f"n_neurons={config.settings['train']['n_neurons']}")
 value=input("Enter the new value: ")
 config.settings["train"]["n_neurons"]=int(value)
 print(f" n_neurons set to {config.settings['train']['n_neurons']}")

def settings_menu():
 menu_labels={
  1:"Game",
  2:"Number of games played to be stored as train data",
  3:"Number of neurons in a hidden layer",
 }
 menu_actions={
  1:choose_game,
  2:set_n_games,
  3:set_n_neurons,
 }
 load_settings()
 while True:
  print("Settings:")
  for i_menu in menu_labels:
   print(f"{i_menu}. {menu_labels[i_menu]}")
  choice=input("Enter your choice, or 0 to return: ")
  if choice=="0":
   break
  action=menu_actions.get(int(choice))
  action()
 save_settings()

def main_menu():
 menu_labels={
  1:"Simulate...",
  2:"Train...",
  3:"Evaluate",
  4:"Optimize",
  5:"Test",
  6:"Settings",
 }
 menu_actions={
  1:simulate_menu,
  2:train_menu,
  3:evaluate_neural_network,
  4:optimize_neural_network,
  5:test_neural_network,
  6:settings_menu,
 }
 while True:
  print("\nMain Menu:")
  print("----------")
  for i_menu in menu_labels:
   print(f"{i_menu}. {menu_labels[i_menu]}")
  choice=input("Enter your choice, or 0 to return: ")
  print()
  if choice=="0":
   break
  action=menu_actions.get(int(choice))
  action()

if __name__=="__main__":
 config.load_settings()
 main_menu()