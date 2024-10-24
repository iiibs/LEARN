import torch
from datetime import datetime

import config
from PerfectPlayer import *
from Game import *
from Simulate import *

class NeuralPlayer:
 def __init__(self,model):
  self.name="neural"
  self.model=model

 def choose_move(self,game):
  input=torch.FloatTensor(game.get_board_as_input()).unsqueeze(0).to(self.model.device)
  with torch.no_grad():
   output=self.model(input).squeeze()
  # Normalize the output to get probabilities
  n_rows=config.settings["game"]["n_rows"]
  n_cols=config.settings["game"]["n_cols"]
  probabilities=torch.nn.functional.softmax(output,dim=0).reshape(n_rows,n_cols)
  # Print the probabilities with one digit after the decimal point
  if config.settings["details"]:
   print("Probabilities:")
   for row in probabilities:
    print(' '.join(f"{cell:.4f}" for cell in row))
  move=output.argmax().item()
  row,col=divmod(move,n_cols)
  while not game.make_move(row,col):
   output[move]=-float('inf')
   move=output.argmax().item()
   row,col=divmod(move,n_cols)
  return (row,col)
