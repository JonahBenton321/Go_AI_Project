import random

import numpy as np
import sente
from scipy.ndimage import convolve
from sente import sgf, stone
import torch
from GoPolicyNet import GoPolicyResNet

#model = GoPolicyResNet()
#best_model = GoPolicyResNet()
#color = sente.WHITE # default to white

class AIHandler: # Main class which handles interaction with the systems AI models

    def __init__(self, model_path,):
        self.model = GoPolicyResNet()
        state_dict = torch.load(model_path, weights_only=True)
        self.model.load_state_dict(state_dict)

        self.best_model = GoPolicyResNet()
        state_dict = torch.load('Go_model_8d.pth', weights_only=True) # This is the model trained on the highest skill level
        self.best_model.load_state_dict(state_dict)

        self.color = sente.WHITE  # default to white

    def set_main_model(self, model_name): # Allows switching models at any point
        state_dict = torch.load(model_name, weights_only=True)
        self.model.load_state_dict(state_dict)

    def set_color(self, new_color):
        self.color = new_color



    # Returns a numpy array which contains all possible moves
    # Array is in best to worst order (best move is at index 0)
    # A moves are single integers like '288' not coordinates
    def infer_distribution(self, game, current_model=None):
        if current_model is None:
            current_model = self.model

        board = game.numpy()

        if game.get_active_player() == stone.WHITE: # Flips white and black stones if its white's turn
            board = np.stack([board[..., 1], board[..., 0], board[..., 2], board[..., 3]], axis=2)

        input_data = torch.from_numpy(board).permute(2, 0, 1).float().unsqueeze(0)

        with torch.inference_mode():
            output = current_model(input_data)
            dist = torch.topk(output, k=361, dim=1)

            return dist[1].numpy()[0] # Returns allow the list of moves removing the tensor

    # Returns the model's best predicted move as tuple where index 0 is x and index y is 1
    # Returned move is always legal
    def infer_best_move(self, game, total_moves=0, current_model=None, random_skip=True):
        if current_model is None:
            current_model = self.model

        move_dist = self.infer_distribution(game, current_model=current_model)
        score_estimate = self.estimate_score(game)

        if self.color == stone.BLACK: # Helps to flip score estimation if model is black
            score_estimate*=-1

        # Causes the model to resign or pass if it is late in the game and the model is losing
        if score_estimate > 20 and total_moves > 150:
            return 'resign'

        if score_estimate > 15 and total_moves > 150:
            return 'pass'

        for move in move_dist: # Loops over all move until a legal move is found
            # Translates a move as a single integer to coordinate e.g. 288 becomes x=3, y=15
            skips=0
            y=int(move/19)
            x = move-(y*19)
            x+=1
            y+=1
            if (random.randint(1,10) > 8 and skips < 6) and random_skip:
                skips+=1
                continue
            skips=0
            if game.is_legal(x,y):
                return int(x), int(y)

    def recommend_move(self, game): # Return the move the best model would play
        return self.infer_best_move(game, current_model=self.best_model, random_skip=False)

    # Returns where to user's move falls in the model's predicted distribution
    # If the user picked what the model thinks is the best move then the play is given rank 0
    def find_rank_in_distribution(self, distribution, move):
        x,y = move
        x-=1
        y-=1
        translated_move = (y*19)+x
        index = np.where(distribution == translated_move)

        if index[0].size == 0: # If move is not in the distribution return the worst possible rating
            return distribution.size - 1

        return index[0][0]

    # Returns a label for the quality of the user's move
    def rate_move(self, distribution, move):
        rank = self.find_rank_in_distribution(distribution, move)

        if rank < 21:
            return 'Excellent '+str(rank)
        elif rank < 201:
            return 'Mediocre '+str(rank)
        else:
            return 'Blunder '+str(rank)

    def rate_user_move(self, game, move): # Must be called before updating sente with the users move
        return self.rate_move(self.infer_distribution(game, current_model=self.best_model), move)

    # Implementation of 'Bouzy's Algorithm' to estimate the score of the game
    # The algorithm was recommended and explained in part by AI
    # The code here is based on the AI description of the algorithm and uses the AI recommended kernal, convolve, and threshold level (0.2)
    # However the code is unique to our system because of how sente handle's the board internally
    # All code was written by hand
    def create_score_heat_map(self, game):
        board_array = np.zeros((19, 19))
        board_array[game.numpy()[:, :, 0] == 1] = 1 # Black stones are 1
        board_array[game.numpy()[:, :, 1] == 1] = -1 # White stones are -1

        heat_map = board_array.copy()
        #print(heat_map)

        kernal = np.array([
            [0.0, 0.1, 0.0],
            [0.1, 1, 0.1],
            [0.0, 0.1, 0.0]
        ])

        for i in range(5):
            heat_map = convolve(heat_map, kernal, mode='constant', cval=0.0)
            heat_map[board_array == 1] = 1.0
            heat_map[board_array == -1] = -1.0

        return heat_map

    # Uses the territory heat map to estimate the score of the game and return
    def estimate_score(self, game):
        territory_map = self.create_score_heat_map(game)
        black = np.sum(territory_map > 0.2)
        white = np.sum(territory_map < -0.2)
        return black-white

    def estimate_score_both_colors(self, game):
        territory_map = self.create_score_heat_map(game)
        black = np.sum(territory_map > 0.2)
        white = np.sum(territory_map < -0.2)
        return str(black)+' Estimated', str(white)+' Estimated'