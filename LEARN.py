import numpy as np
from datetime import datetime
import json

import config
from Train import *
from PerfectPlayer import *
from NeuralPlayer import *
from NeuralNetwork import *
from HumanPlayer import *
from Evaluate import *

def f(x,y):
 train=Train()
 max_points=0
 n_trains=config.settings["train"]["n_trains"]
 i_train=1
 while True:
  max_points=train.run(max_points)
  i_train+=1
  if i_train>n_trains:
   break
 return max_points

def new_pos(x0,y0,delta_x,max_n_neurons,resolution):
 grad_horiz_plus=f(x0+delta_x,y0)
 grad_horiz_minus=f(x0-delta_x,y0)
 grad_horiz=(grad_horiz_plus-grad_horiz_minus)/(2*delta_x)
 delta_y=max_n_neurons/resolution
 grad_vert_plus=f(x0,y0+delta_y)
 grad_vert_minus=f(x0,y0-delta_y)
 grad_vert=(grad_vert_plus-grad_vert_minus)/(2*delta_y)
 eta=1/resolution
 x1=x0+eta*grad_horiz
 y1=y0+eta*grad_vert
 return x1,y1

def teach_neural_network_old():
 print(f"Teaching started at: {current_time}")
 resolution=8
 min_n_games=config.n_games/2
 max_n_games=config.n_games+min_n_games
 delta_x=max_n_games/resolution
 min_n_neurons=config.n_neurons/2
 max_n_neurons=config.n_neurons+min_n_neurons
 x0=config.n_games
 y0=config.n_neurons
 x1=x0
 y1=y0
 config.max_z=0
 i_step=1
 while True:
  z=f(x0,y0)
  if z>config.max_z:
   config.max_z=z
  i_step+=1
  if i_step>config.n_steps:
   break
  x1,y1=new_pos(x0,y0,delta_x,max_n_neurons,resolution)
  x0=x1
  y0=y1
  print(f"(x0,y0)=({x0},{y0}) -> max(f(x0,y0))={max_z}")
 print(f"final position and maximum value (x,y): ({x1}, {y1}) -> {config.max_z}")
 print(f"it means that")
 print(f" - n_games should be {round(x1)}, and")
 print(f" - n_neurons should be {round(y1)}.")
 return

def teach_neural_network():
 current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 print(f"Teaching started at: {current_time}")
 x=config.settings["train"]["n_games"]
 y=config.settings["train"]["n_neurons"]
 config.settings["teach"]["f"]["max_z"]=0
 n_steps=config.settings["teach"]["n_steps"]
 i_step=1
 while True:
  z=f(x,y)
  i_step+=1
  if i_step>n_steps:
   break
  print(f"(x,y)=({x},{y}) -> max(f(x,y))={z}")
 print(f"after {n_steps} steps the final maximum value (x,y): ({x}, {y}) -> {z}")
 current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 print(f"Teaching ended at: {current_time}")
 return

def train_neural_network():
 current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 print(f"Training started at: {current_time}")
 train=Train()
 train.run()

def evaluate_neural_network():
 model=NeuralNetwork()
 evaluate=Evaluate(model)
 performance=evaluate.run()
 performance_neural_vs_perfect=performance["performance_neural_vs_perfect"]
 performance_neural_vs_random=performance["performance_neural_vs_random"]
 performance_perfect_vs_random=performance["performance_perfect_vs_random"]
 b_evaluation= \
  round(performance_neural_vs_perfect)==100 and \
  round(performance_neural_vs_random)>=round(performance_perfect_vs_random)
 if b_evaluation:
  print(f"Neural network evaluation success.")
 else:
  print(f"Neural network evaluation fail.")
 return b_evaluation

def test_neural_network():
 human_player=HumanPlayer()
 model=NeuralNetwork()
 neural_player=NeuralPlayer(model)
 neural_player.model.load_state_dict(torch.load(model.best_filename))
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
 b_details_save=config.b_details
 config.b_details=True
 game_data=game.play()
 if game.winner_symbol=='':
  print("draw")
 elif game.winner_symbol=='X':
  print(f"{game.first_player} won.")
 elif game.winner_symbol=='O':
  print(f"{game.second_player} won.")
 config.b_details=b_details_save
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

def set_repeatable_random(repeatable):
 if repeatable:
  np.random.seed(0)
  #np.random.seed(None)
  #np.random.seed(42)
  #np.random.seed(1) # draw
  #np.random.seed(2)
  #np.random.seed(3)

set_repeatable_random(False) # True False
config.b_details=False

def load_settings():
 try:
  with open("settings.json","r") as f:
   config.settings=json.load(f)
 except FileNotFoundError:
  save_settings()

def save_settings():
 with open("settings.json","w") as f:
  json.dump(config.settings,f,indent=1)

def set_game(id):
 current_gameid=id-1
 config.settings["gameid"]=current_gameid
 current_game=next(game for game in config.settings["games"] if game["id"]==current_gameid)
 current_game_name=current_game["name"]
 config.settings["game"]["name"]=current_game_name
 current_game_empty_cell_symbol=current_game["empty_cell_symbol"]
 config.settings["game"]["empty_cell_symbol"]=current_game_empty_cell_symbol
 current_game_n_rows=current_game["n_rows"]
 config.settings["game"]["n_rows"]=current_game_n_rows
 current_game_n_cols=current_game["n_cols"]
 config.settings["game"]["n_cols"]=current_game_n_cols
 print(f"Game set to {current_game_name}.")

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
 load_settings()
 menu_labels={
  1:"Train",
  2:"Evaluate",
  3:"Test",
  4:"Settings",
 }
 menu_actions={
  1:train_neural_network,
  2:evaluate_neural_network,
  3:test_neural_network,
  4:settings_menu,
 }
 while True:
  print("Main Menu:")
  for i_menu in menu_labels:
   print(f"{i_menu}. {menu_labels[i_menu]}")
  choice=input("Enter your choice, or 0 to return: ")
  if choice=="0":
   break
  action=menu_actions.get(int(choice))
  action()

if __name__=="__main__":
 main_menu()