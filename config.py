import json

settings= \
{
 "details": False,
 "games": [
  {
   "id":0,
   "name":"tic-tac-toe",
   "n_rows": 3,
   "n_cols": 3,
   "expected_points_as_first": 0.5,
   "simulate_games": 1000000,
   "train_neurons": 100
  },
  {
   "id":1,
   "name":"OXXO",
   "n_rows": 1,
   "n_cols": 4,
   "expected_points_as_first": 1.0,
   "simulate_games": 195,
   "train_neurons": 5
  },
 ],
 "gameid":0, # this stores the id of the actual game that we are dealing with currently
 "game": {
  "name": "",
  "n_rows": 0,
  "n_cols": 0,
  "expected_points_as_first": 0.0, # the first player of a game can earn this point value (when twop perfect players are playing)
 },
 "simulate": {
  "save_interval_seconds": 3600, # if this is 3600, then it will save training data every hour
  "n_games": 1000000, # Number of games to be played between random and perfect - creates the database for RL
  "n_games_saved": 0, # Number of games saved at the last saving point, in case of "Continue Simulation" only n_games_total-n_games_saved will be played
 },
 "train": {
  "save_interval_seconds": 3600,
  "n_neurons": 10, # number of neurons in one layer of the 1 + 3 + 1 layer neural network
  "n_epochs": 10, # number of epochs run in one learning step
  "win_value": 1.0,
  "draw_value": 0.5,
  "loss_value": 0.0,
  "n_epochs_saved": 0,
 },
 "network": {
  "learning_rate": 0.001,
  "heartbeat_rate": 1,
 },
 "evaluate": {
  "n_games": 1000
 },
 "optimize": {
  "min_games": 10,
  "max_games": 1000,
  "min_neurons": 4,
  "max_neurons": 12,
 },
}

b_details=True #True #False

def set_repeatable_random(repeatable):
 if repeatable:
  np.random.seed(0)
  #np.random.seed(None)
  #np.random.seed(42)
  #np.random.seed(1) # draw
  #np.random.seed(2)
  #np.random.seed(3)

empty_cell_symbol="-"

def opponent(symbol):
 if symbol=='X':
  return 'O'
 if symbol=='O':
  return 'X'
 return ''

def save_settings():
 global settings
 with open("settings.json","w") as f:
  json.dump(settings,f,indent=1)

def load_settings():
 global settings
 try:
  with open("settings.json","r") as f:
   settings=json.load(f)
 except FileNotFoundError:
  create_settings()

def create_settings():
 global settings
 set_game(settings["gameid"]+1)
 save_settings()

def set_game(id):
 global settings
 current_gameid=id-1
 settings["gameid"]=current_gameid
 current_game=next(game for game in settings["games"] if game["id"]==current_gameid)
 current_game_name=current_game["name"]
 settings["game"]["name"]=current_game_name
 current_game_n_rows=current_game["n_rows"]
 settings["game"]["n_rows"]=current_game_n_rows
 current_game_n_cols=current_game["n_cols"]
 settings["game"]["n_cols"]=current_game_n_cols
 current_game_expected_points_as_first=current_game["expected_points_as_first"]
 settings["game"]["expected_points_as_first"]=current_game_expected_points_as_first
 print(f"Game set to {current_game_name}.")
 settings["simulate"]["n_games"]=settings["games"][current_gameid]["simulate_games"]
 settings["train"]["n_neurons"]=settings["games"][current_gameid]["train_neurons"]

