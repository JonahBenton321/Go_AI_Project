from pathlib import Path
import numpy as np
import sente
from sente import sgf, stone
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
from GoPolicyNet import GoPolicyResNet
np.set_printoptions(threshold=np.inf, linewidth=np.inf)
model = GoPolicyResNet()
state_dict = torch.load('Go_Model_8d.pth', weights_only=True)
model.load_state_dict(state_dict)
game = sgf.load(r'C:\Users\Jonah Benton\Downloads\8k2\8d\1450096422019999389.sgf', ignore_illegal_properties=True, fix_file_format=True, disable_warnings=True)
sequence = game.get_default_sequence()


class AI_hanndler():
    def __init__(self):
        self.model=model


    def infer_distubution(self, game):
        board = game.numpy()
        input_data = torch.from_numpy(board).permute(2, 0, 1).float().unsqueeze(0)
        with torch.inference_mode():
            output = model(input_data)
            dist = torch.topk(output, k=361, dim=1)
            return dist[1].numpy()[0]

    def infer_best_move(self, game):
        move_dist = self.infer_distubution(game)
        for move in move_dist:
            y=int(move/19)
            x = move-(y*19)
            print(move, x, y)
            if game.is_legal(x,y):
                return x, y
        return -1
'''
model.eval()
game.play_sequence(sequence[:50])
board = game.numpy()

if game.get_active_player() == stone.WHITE:  # Flips white and black stones if its white's turn
    board = np.stack([board[..., 1], board[..., 0], board[..., 2], board[..., 3]], axis=2)
    
input_data = torch.from_numpy(board).permute(2, 0, 1).float().unsqueeze(0)
with torch.inference_mode():
    output = model(input_data)
    print(torch.topk(output, k=5, dim=1))

#game.play(sequence[3])
print(game)
print(sequence[50].get_x(),sequence[50].get_y())
game.advance_to_root()
game.play_sequence(sequence[:51])
print(game)
'''