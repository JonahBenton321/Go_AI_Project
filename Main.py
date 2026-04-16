from pathlib import Path

from pathlib import Path
import numpy as np
import sente
from sente import sgf, stone
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
from GoPolicyNet import GoPolicyResNet
from model_handler import AIHandler

# right now main is test ground for ideas like the model playing itself

'''
game.advance_to_root()
game.play_sequence(sequence[:len(sequence)])
move = AI.infer_best_move(game)
print(game)
print(move)
'''

'''
game.advance_to_root()
for i in range(len(sequence)):
    print(game)
    move = AI.infer_best_move(game)
    print(move)
    game.play(sequence[i])
'''

'''
for i in range(250):
    #print(game)
    move = AI.infer_best_move(game)
    #print(move)
    game.play(move[0], move[1])
print(game)
'''