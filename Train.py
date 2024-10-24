import torch

import config
from Simulate import *
from NeuralNetwork import *

class Train:
 def __init__(self,filename='tictactoe_nn.pth'):
  self.filename=filename
  self.n_neurons=config.settings["train"]["n_neurons"]
  self.n_epochs=config.settings["train"]["n_epochs"]
  self.save_interval_seconds=config.settings["train"]["save_interval_seconds"]
  self.should_continue=True
  self.should_save=False
  self.max_points=0
  self.simulate=Simulate()
  self.model=NeuralNetwork()
  self.n_epochs=config.settings["train"]["n_epochs"]
  self.heartbeat_rate=config.settings["network"]["hearbeat_rate"]

 def interrupt_and_set_save(self):
  while self.should_continue:
   time.sleep(self.save_interval_seconds)
   self.should_save=True

 def run(self,mode):
  file_path=self.filename

  # Load the simulated data.
  self.simulate.load_training_data_from_file()
  print(f'Game data loaded from {self.simulate.filename}')
  if config.settings["details"]:
   self.print_game_data()
  self.n_training_data_items=len(self.simulate.training_data)
  print(f" with n_training_data_items= {self.n_training_data_items}, n_neurons= {self.n_neurons}")

  # Start a new training.
  if mode=="new":
   if os.path.exists(file_path):
    os.remove(file_path)
    print(f"Trained model {file_path} deleted.")
   else:
    print(f"Trained model {file_path} did not exist.")

  # Continue an earlier saved training.
  if mode=="continue":
   if os.path.exists(file_path):
    self.load_model_weights_from_file()
    print(f"Model weights {file_path} loaded.")
    config.load_settings()
    self.n_epochs_saved=config.settings["train"]["n_epochs_saved"]
    print(f"{self.n_epochs_saved} epochs already saved.")

  interrupt_thread=threading.Thread(target=self.interrupt_and_set_save)
  while self.should_continue==True:
   interrupt_thread.start()
   # Train neural network.
   data=self.simulate.training_data
   self.model=self.train_model(data)
   interrupt_thread.join()

  # Save the settings and the trained neural network model.
  config.save_settings()
  self.save_model_weights_to_file()
  current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  print(f"all {n_epochs} epochs saved at: {current_time}.")
  return

 def train_model(self,training_data):
  criterion=nn.MSELoss()
  optimizer=optim.Adam(self.model.parameters(),lr=config.settings["network"]["learning_rate"])
  for i_epoch in range(self.n_epochs_saved,self.n_epochs):
   total_loss=0
   for flat_input,flat_target in training_data:
    input=torch.FloatTensor(flat_input).unsqueeze(0).to(self.model.device)
    target=torch.FloatTensor(flat_target).unsqueeze(0).to(self.model.device)
    optimizer.zero_grad()
    output=self.model(input)
    loss=criterion(output,target)
    loss.backward()
    optimizer.step()
    total_loss+=loss.item()
   if(i_epoch+1)%self.heartbeat_rate==0:
    current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{current_time} - Epoch {i_epoch + 1}, Loss: {total_loss / len(training_data):.2f}')
    config.settings["train"]["n_epochs_saved"]=i_epoch+1
    config.save_settings()
    self.save_model_weights_to_file()
  return self.model

 def save_model_weights_to_file(self):
  # Save the weights of a neural network model.
  torch.save(self.model.state_dict(),self.model.filename)
  # Save the already completed epochs in config settings.
  n_epochs_saved=config.settings["train"]["n_epochs_saved"]
  config.save_settings()
  current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  print(f"n_epochs_saved/n_epochs: {n_epochs_saved}/{self.n_epochs}, time: {current_time}")
  self.should_save=False
  return
 
 def load_model_weights_from_file(self):
  # Load a saved neural network.
  self.model.load_state_dict(torch.load(self.model.filename))
  config.load_settings()
  return

 def print_game_data(self):
  for i,(input,target) in enumerate(self.simulate.training_data):
   print(input)
   print(target)
  return

