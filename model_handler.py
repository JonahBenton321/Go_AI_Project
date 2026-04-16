import numpy as np
import sente
from scipy.ndimage import convolve
from sente import sgf, stone
import torch
from GoPolicyNet import GoPolicyResNet

model = GoPolicyResNet()
best_model = GoPolicyResNet()
color = sente.WHITE # default to white

class AIHandler:

    def __init__(self, model_path):
        state_dict = torch.load(model_path, weights_only=True)
        model.load_state_dict(state_dict)

        state_dict = torch.load(model_path, weights_only=True) # right now the "best model" is the only model we have. this NEEDS to be fixed in the future
        best_model.load_state_dict(state_dict)

    def set_main_model(self, model_name):
        state_dict = torch.load('Go_Model_8d.pth', weights_only=True)
        model.load_state_dict(state_dict)

    def infer_distubution(self, game, current_model=model):
        board = game.numpy()

        if game.get_active_player() == stone.WHITE: # Flips white and black stones if its white's turn
            board = np.stack([board[..., 1], board[..., 0], board[..., 2], board[..., 3]], axis=2)

        input_data = torch.from_numpy(board).permute(2, 0, 1).float().unsqueeze(0)

        with torch.inference_mode():
            output = current_model(input_data)
            dist = torch.topk(output, k=361, dim=1)

            return dist[1].numpy()[0]

    def infer_best_move(self, game, total_moves=0, current_model=model):
        move_dist = self.infer_distubution(game, current_model=model)
        score_estimate = self.estimate_score(game)

        if color == stone.WHITE:
            score_estimate*=-1

        if score_estimate > 20 and total_moves > 150:
            return 'resign'

        if score_estimate > 10 and total_moves > 150:
            return 'pass'

        for move in move_dist:
            y=int(move/19)
            x = move-(y*19)

            if game.is_legal(x,y):
                return x, y

    def recommend_move(self, game):
        return self.infer_best_move(game, current_model=best_model)

    def find_rank_in_distribution(self, distribution, move):
        translated_move = (move[0]*19)+move[1]
        index = np.where(distribution == translated_move)

        if index[0].size == 0: # If move is not in the distribution return the worst possible rating
            return distribution.size - 1

        return index[0]

    def rate_move(self, distribution, move):
        rank = self.find_rank_in_distribution(distribution, move)

        if rank < 6:
            return 'Excellent'
        elif rank < 51:
            return 'Mediocre'
        else:
            return 'Blunder'

    def rate_user_move(self, game, move): # Must be called before updating sente with the users move
        return self.rate_move(self.infer_distubution(game), move)

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

    def estimate_score(self, game):
        territory_map = self.create_score_heat_map(game)
        black = np.sum(territory_map > 0.2)
        white = np.sum(territory_map < -0.2)
        return black-white
