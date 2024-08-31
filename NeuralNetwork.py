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

 def forward(self,x):
  x=self.relu(self.fc1(x))
  x=self.relu(self.fc2(x))
  x=self.relu(self.fc3(x))
  x=self.relu(self.fc4(x))
  x=self.fc5(x)
  return x

def train_model(model,training_data):
 criterion=nn.MSELoss()
 optimizer=optim.Adam(model.parameters(),lr=0.001)
 heartbeat_rate=config.n_epochs/10
 for epoch in range(config.n_epochs):
  total_loss=0
  for flat_input,flat_target in training_data:
   input=torch.FloatTensor(flat_input).unsqueeze(0).to(model.device)
   target=torch.FloatTensor(flat_target).unsqueeze(0).to(model.device)
   optimizer.zero_grad()
   output=model(input)
   loss=criterion(output,target)
   loss.backward()
   optimizer.step()
   total_loss+=loss.item()
  if (epoch + 1) % heartbeat_rate == 0:
   current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   if config.b_details:
    print(f'{current_time} - Epoch {epoch + 1}, Loss: {total_loss / len(training_data):.2f}')
 return model
