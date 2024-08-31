settings= \
{
 "details": True,
 "games": [
  {
   "id":0,
   "name":"tic-tac-toe",
   "empty_cell_symbol":"-",
   "n_rows": 3,
   "n_cols": 3,
   "expected_points_as_first": 0.5,
  },
  {
   "id":1,
   "name":"OXXO",
   "empty_cell_symbol":"-",
   "n_rows": 1,
   "n_cols": 4,
   "expected_points_as_first": 1.0,
  },
 ],
 "gameid":0,
 "game": {
  "name": "OXXO",
  "empty_cell_symbol": "-",
  "n_rows": 1,
  "n_cols": 4,
  "expected_points_as_first": 1.0, # the first player of a game can earn this point value (when twop perfect players are playing)
 },
 "train": {
  "new": True,
  "n_games": 10, # Number of games to be played between random and perfect - creates the database for RL
  "n_neurons": 10, # number of neurons in one layer of the 1 + 3 + 1 layer neural network
  "win_value": 1.0,
  "draw_value": 0.5,
  "loss_value": 0.0,
  "n_eval_games": 100, # number of games during evaluation
  "n_trains": 2,
 },
 "teach": {
  "n_steps": 1, # Number of steps that the gradient method will perform in two dimensions to reach the highest point
  "f": {
   "z": 0, # value of the f function at (x,y) point
   "max_z": 0, # maximum z value so far
  },
 },
}

n_epochs=10 # 10 epochs will be trained
b_new_train_data=True # should we generate new training data?
b_new_train=True # should we perform a new train?
#n_repetitions=5 # we need to repeat the training, because the number of draws can be different
n_steps=10 # we perform this many steps toward the optimum

n_evaluations=100

create_nn=False #False #True

evaluate_nn=True #True #False

b_details=True #True #False

def opponent(symbol):
 if symbol=='X':
  return 'O'
 if symbol=='O':
  return 'X'
 return ''

