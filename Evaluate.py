import torch

import config
from PerfectPlayer import *
from RandomPlayer import *
from NeuralPlayer import *
from HumanPlayer import *
from Game import *
from Simulate import *
from NeuralNetwork import *

class Evaluate:
 def __init__(self,model):
  self.model=model
  self.n_games=config.settings["evaluate"]["n_games"]
  self.max_points=0

 def run(self):
  current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  print(f'Evaluation started at: {current_time}')
  print(f" with n_games= {self.n_games}")
  neural_player=NeuralPlayer(self.model)
  neural_player.model.load_state_dict(torch.load(self.model.filename))
  perfect_player=PerfectPlayer()
  random_player=RandomPlayer()
  performance_neural_vs_perfect=round(100*self.run_games(neural_player,perfect_player))
  if config.settings["details"]:
   print(f"Neural player performance against perfect player was: {performance_neural_vs_perfect}%")
  performance_neural_vs_random=round(100*self.run_games(neural_player,random_player))
  if config.settings["details"]:
   print(f"Neural player performance against random player was: {performance_neural_vs_random}%")
  performance_perfect_vs_random=round(100*self.run_games(perfect_player,random_player))
  if config.settings["details"]:
   print(f"Perfect player performance against random player was: {performance_perfect_vs_random}%")
  performance={ \
   "performance_neural_vs_perfect":performance_neural_vs_perfect, \
   "performance_neural_vs_random":performance_neural_vs_random, \
   "performance_perfect_vs_random":performance_perfect_vs_random}
  if config.settings["details"]:
   print(performance)
  performance_neural_vs_random_relative_to_perfect_vs_random= \
   round(100*performance_neural_vs_random/performance_perfect_vs_random)
  print(f" against perfect directly: {performance_neural_vs_perfect}% "+
        f"against perfect via random: {performance_neural_vs_random_relative_to_perfect_vs_random}%")
  b_success=performance_neural_vs_perfect>=100 and \
            performance_neural_vs_random_relative_to_perfect_vs_random>=100
  current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  print(f'Evaluation ended at: {current_time}')
  return b_success

 def run_games(self,player,evaluator):
  if config.settings["game"]["name"]=="tic-tac-toe":
   game=TictactoeGame(player,evaluator)
  if config.settings["game"]["name"]=="OXXO":
   game=OxxoGame(player,evaluator)
  firsts=0;wins=0;draws=0;losses=0
  for _ in range(self.n_games):
   game.reset(player,evaluator)
   states=game.play()
   if game.first_player==player:
    firsts+=1
   if game.winner_symbol=='':
    if config.settings["details"]:
     print("draw")
    draws+=1
   if game.winner_symbol=='X':
    if config.settings["details"]:
     print(f"{game.first_player} won with X.")
    if game.first_player==player:
     wins+=1
     if game.first_player.name=="neural" and game.second_player.name=="perfect" or \
        game.first_player.name=="perfect" and game.second_player.name=="neural":
      print("Unexpected result.")
    else:
     losses+=1
   if game.winner_symbol=='O':
    if config.settings["details"]:
     print(f"{game.second_player} won with O.")
    if game.second_player==player:
     wins+=1
     if game.first_player.name=="neural" and game.second_player.name=="perfect" or \
        game.first_player.name=="perfect" and game.second_player.name=="neural":
      print("Unexpected result.")
    else:
     losses+=1
  if config.settings["details"]:
   current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print(f'{current_time}')
   print(f"Player played as first in {firsts}/{self.n_games} games and won {wins}, tied {draws}, lost {losses}.")
  seconds=self.n_games-firsts
  expected_points_as_first=config.settings["game"]["expected_points_as_first"]
  expected_points_as_second=1.0-expected_points_as_first
  expected_points=firsts*expected_points_as_first+seconds*expected_points_as_second
  actual_points= \
   wins*config.settings["train"]["win_value"]+ \
   draws*config.settings["train"]["draw_value"]+ \
   losses*config.settings["train"]["loss_value"]
  if actual_points==expected_points:
   return 1.0
  else:
   if expected_points==0 and actual_points>0:
    return 9.99 # theoretical value to avoid division by zero
   else:
    return actual_points/expected_points
