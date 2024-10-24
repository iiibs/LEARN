import torch
import torch.nn as nn
import torch.optim as optim
from datetime import datetime

import config

class NeuralNetwork(nn.Module):
 def __init__(self):
  super(NeuralNetwork,self).__init__()
  n_input_neurons=config.settings["game"]["n_rows"]*config.settings["game"]["n_cols"]
  n_neurons=config.settings["train"]["n_neurons"]
  self.fc1=nn.Linear(n_input_neurons,n_neurons)
  self.fc2=nn.Linear(n_neurons,n_neurons)
  self.fc3=nn.Linear(n_neurons,n_neurons)
  self.fc4=nn.Linear(n_neurons,n_neurons)
  n_output_neurons=n_input_neurons
  self.fc5=nn.Linear(n_neurons,n_output_neurons)
  self.relu=nn.ReLU()
  if config.settings["game"]["name"]=="tic-tac-toe":
   self.filename='tictactoe_nn.pth'
   self.best_filename='tictactoe_nn_best.pth'
  if config.settings["game"]["name"]=="OXXO":
   self.filename='oxxo_nn.pth'
   self.best_filename='oxxo_nn_best.pth'
  self.device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
  self.to(self.device)
  return

 def forward(self,x):
  x=self.relu(self.fc1(x))
  x=self.relu(self.fc2(x))
  x=self.relu(self.fc3(x))
  x=self.relu(self.fc4(x))
  x=self.fc5(x)
  return x
