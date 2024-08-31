<style>
body {
    background-color: #000;
    color: #fff;
}
</style>

# Learn
A program that trains a neural network player, which learns\
 from a perfect player how to play a simple board game (tic-tac-toe or OXXO) perfectly.

## Games
 The well known tic-tac-toe game and the very simple OXXO game.\
 Both players have draw strategy.

 OXXO is played on a 1 by 4 board, and the player who has\
 two consecutive symbols of their own is the winner.\
 The first player has winning strategy.

## Neural network
 Input layer: a board state\
 Three hidden layers: each of them with n_neurons

## Training
 n_number of sample games are played between Perfect and Random players.\
 The neural network will be trained on this training set of games, and\
  the Neural player will use this trained neural network.

## Evaluation
 The Neural player will play autonomously evaluation games against\
  the Perfect player and the Random player.\
 If both results are as good as the results of the Perfect player, then\
 the evaluation is a success, otherwise it is a fail.

## Test
 Human player can test the Neural player to get a human verification\
  that the Neural player has really learned the perfect strategy of the game.
