import numpy as np
import random

import config

class PerfectPlayer:
 def __init__(self):
  self.symbol=""
  self.opponent_symbol=""
  self.empty_cell_symbol=config.settings["game"]["empty_cell_symbol"]

 def choose_move(self,game):
  if config.settings["game"]["name"]=="tic-tac-toe":
   # Check if the board is empty
   if np.all(game.board.cells==self.empty_cell_symbol):
    # Choose a random move if the board is empty
    return random.choice(self.get_possible_moves(game))

   # Check if we are right after the opponent's opening
   if np.sum(game.board.cells==self.opponent_symbol)==1:
    opponents_opening_move=game.get_opponents_opening_move(self.opponent_symbol)
    # Was it a corner oopening?
    if \
     opponents_opening_move==(0,0) or \
     opponents_opening_move==(0,2) or \
     opponents_opening_move==(2,0) or \
     opponents_opening_move==(2,2):
     # Respond with a center cell.
     return (1,1)
    # Was it a center oopening?
    if opponents_opening_move==(1,1):
     # Respond with a random corner cell.
     best_moves=[]
     best_moves.append((0,0))
     best_moves.append((0,2))
     best_moves.append((2,0))
     best_moves.append((2,2))
     return random.choice(best_moves)
    # Was it an upper edge oopening?
    if opponents_opening_move==(0,1):
     best_moves=[]
     # Respond with either a center cell
     best_moves.append((1,1))
     # Or respond with a corner cell next to the opponent's cell
     best_moves.append((0,0))
     best_moves.append((0,2))
     # Or respond with the edge opposite to the opponent's cell
     best_moves.append((2,1))
    # Was it a left edge oopening?
    if opponents_opening_move==(1,0):
     best_moves=[]
     # Respond with either a center cell
     best_moves.append((1,1))
     # Or respond with a corner cell next to the opponent's cell
     best_moves.append((0,0))
     best_moves.append((2,0))
     # Or respond with the edge opposite to the opponent's cell
     best_moves.append((1,2))
    # Was it a right edge oopening?
    if opponents_opening_move==(1,2):
     best_moves=[]
     # Respond with either a center cell
     best_moves.append((1,1))
     # Or respond with a corner cell next to the opponent's cell
     best_moves.append((0,2))
     best_moves.append((2,2))
     # Or respond with the edge opposite to the opponent's cell
     best_moves.append((1,0))
    # Was it a lower edge oopening?
    if opponents_opening_move==(2,1):
     best_moves=[]
     # Respond with either a center cell
     best_moves.append((1,1))
     # Or respond with a corner cell next to the opponent's cell
     best_moves.append((2,0))
     best_moves.append((2,2))
     # Or respond with the edge opposite to the opponent's cell
     best_moves.append((0,1))
     return random.choice(best_moves)
        
   best_moves=[]
   best_score=-float('inf')
        
   for move in self.get_possible_moves(game):
    row,col=move
    game.make_move(row,col)
    score=self.minimax(game,False)
    game.board.cells[row,col]=self.empty_cell_symbol
        
    if score>best_score:
     best_score=score
     best_moves=[move]
    elif score==best_score:
     best_moves.append(move)

   return random.choice(best_moves)

  if config.settings["game"]["name"]=="OXXO":
   best_moves=[]
   best_score=-float('inf')
   for move in self.get_possible_moves(game):
    row,col=move
    game.make_move(row,col)
    score=self.minimax(game,False)
    game.board.cells[row,col]=self.empty_cell_symbol
    if score>best_score:
     best_score=score
     best_moves=[move]
    elif score==best_score:
     best_moves.append(move)
   return random.choice(best_moves)

 def minimax(self, game, is_maximizing):
        # Terminal state check
        if game.is_game_over():
            return self.evaluate_board(game)
        
        if is_maximizing:
         # The last move was performed by the opponent, so the algorithm tries to find the maximum score from here

            best_score=-float('inf')
            for move in self.get_possible_moves(game):
                row,col=move
                game.put_symbol_at(self.symbol,row,col)
                score=self.minimax(game,False)
                game.board.cells[row,col]=self.empty_cell_symbol
                best_score=max(best_score,score)
            return best_score
        else:
         # The last move was performed by PerfectPlayer, so the algorithm tries to find the minimum score from here
            best_score=float('inf')
            for move in self.get_possible_moves(game):
                row,col=move
                game.put_symbol_at(self.opponent_symbol,row,col)
                score=self.minimax(game,True)
                game.board.cells[row,col]=self.empty_cell_symbol
                best_score=min(best_score,score)
            return best_score

 def get_possible_moves(self, game):
        possible_moves=[]
        for row in range(config.settings["game"]["n_rows"]):
            for col in range(config.settings["game"]["n_cols"]):
                if game.board.cells[row,col]==config.settings["game"]["empty_cell_symbol"]:
                    possible_moves.append((row,col))
        return possible_moves

 def evaluate_board(self, game):
        # Return the proper value of the game
        if game.is_winner(self.symbol):
            return config.settings["train"]["win_value"]
        elif game.is_winner(self.opponent_symbol):
            return config.settings["train"]["loss_value"]
        else:
            return config.settings["train"]["draw_value"]
