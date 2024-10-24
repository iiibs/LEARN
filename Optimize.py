import torch
import json

import config
from NeuralNetwork import *
from Evaluate import *
from Train import *

class Optimize:
 def __init__(self):
  self.min_games=config.settings["optimize"]["min_games"]
  self.max_games=config.settings["optimize"]["max_games"]
  self.min_neurons=config.settings["optimize"]["min_neurons"]
  self.max_neurons=config.settings["optimize"]["max_neurons"]
  self.optimal_games=self.max_games
  self.optimal_neurons=self.max_neurons
  self.b_success=False

 def run(self):
  high_games,low_games=self.max_games,self.min_games
  high_neurons,low_neurons=self.max_neurons,self.min_neurons
  dimension="games"
  while low_games+1<high_games or low_neurons+1<high_neurons:
   n_games=(low_games+high_games)//2
   n_neurons=(low_neurons+high_neurons)//2
   config.settings["train"]["n_games"]=n_games
   config.settings["train"]["n_neurons"]=n_neurons
   with open("settings.json","w") as f:
    json.dump(config.settings,f,indent=1)
   train=Train()
   train.run()
   model=NeuralNetwork()
   evaluate=Evaluate(model)
   b_evaluation=evaluate.run()
   if b_evaluation:
    print(f"Evaluation success at ({n_games},{n_neurons}).")
    self.b_success=True
    self.optimal_games=n_games
    self.optimal_neurons=n_neurons
    config.settings["train"]["n_games"]=self.optimal_games
    config.settings["train"]["n_neurons"]=self.optimal_neurons
    with open("settings.json","w") as f:
     json.dump(config.settings,f,indent=1)
    print(f" move towards lower values")
    if dimension=='games':
     high_games=n_games
    else:
     high_neurons=n_neurons
   else:
    print(f"Evaluation fail at ({n_games},{n_neurons}).")
    print(f" move towards higher values")
    if dimension=='games':
     low_games=n_games
    else:
     low_neurons=n_neurons
   if dimension=="games":
    dimension="neurons"
    continue
   if dimension=="neurons":
    dimension="games"
    continue
  return self.b_success,self.optimal_games,self.optimal_neurons
