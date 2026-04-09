import random
import sys
from pathlib import Path

import numpy as np
import sente
from numpy import memmap
from sente import sgf, stone
import traceback



def convert_move_numpy(game):
    game.advance_to_root()
    sequence = game.get_default_sequence()
    #print(len(sequence))

    all_moves = np.zeros((len(sequence)),dtype=np.uint16)
    for i in range(len(sequence)):
        x = sequence[i].get_x()
        y = sequence[i].get_y()
        game.play(sequence[i])
        all_moves[i]=(y*19)+x
    return all_moves



def convert_board_state_to_numpy(game):
    game.advance_to_root()
    sequence = game.get_default_sequence()
    all_board_states = np.zeros((len(sequence), 19, 19, 4), dtype=np.uint8)
    #creats an empty board for the first index
    all_board_states[0, :, :,2]=1

    for i in range(len(sequence)-1):
        game.play(sequence[i])
        board = game.numpy()

        if game.get_active_player() == stone.WHITE:
            board = np.stack([board[..., 1], board[..., 0], board[..., 2], board[..., 3]], axis=2)

        all_board_states[i+1] = board


    return all_board_states

def get_random_legal_move(game):
    attempts=0
    while True:
        attempts+=1
        x = random.randint(0, 18)
        y = random.randint(0, 18)
        if game.is_legal(x, y):
            break
        if attempts>361:
            print(game)
            return 0,0
    return x,y

def create_random_negative_moves(game):
    game.advance_to_root()
    sequence = game.get_default_sequence()
    all_negative_moves=np.zeros((len(sequence), 19, 19), dtype=np.uint8)
    for i in range(len(sequence)):

        x,y = get_random_legal_move(game)
        all_negative_moves[i][y][x]=1


        game.play(sequence[i])

    return all_negative_moves

def create_shifted_negative_moves(game):
    game.advance_to_root()
    sequence = game.get_default_sequence()
    all_negative_moves = np.zeros((len(sequence), 19, 19), dtype=np.uint8)
    for i in range(len(sequence)):
        x = sequence[i].get_x()
        y = sequence[i].get_y()
        shifted_x = [x + 1,x + 2,x - 1,x - 2]
        shifted_x[:] = [e for e in shifted_x if (0 < e < 19)]

        shifted_y = [y + 1, y + 2, y - 1, y - 2]
        shifted_y[:] = [e for e in shifted_y if 0 < e < 19]

        all_shifts = []
        for x in shifted_x:
            for y in shifted_y:
                all_shifts.append([x,y])

        all_shifts[:] = [e for e in all_shifts if game.is_legal(e[0], e[1])]
        if not all_shifts:
            random_move = random.choice(get_random_legal_move(game))
            all_negative_moves[i][random_move[1]-1][random_move[0]-1]=1
            all_negative_moves[i][0][0] = 1
        else:

            random_move = random.choice(all_shifts)
            all_negative_moves[i][random_move[1]][random_move[0]]=1
    return all_negative_moves




def create_x_data_parings(game):
    game.advance_to_root()
    length = len(game.get_default_sequence())

    x_data_positive = np.zeros((length, 19,19,5), dtype=np.uint8)

    board_state=convert_board_state_to_numpy(game)
    move=convert_move_numpy(game)

    x_data_positive[:, :, :, :4] = board_state
    x_data_positive[:, :, :, 4] = move

    x_data_negative = np.zeros((length, 19,19,5), dtype=np.uint8)

    x_data_negative[:length, :, :, :4] = board_state
    x_data_negative[:length, :, :, 4] = create_random_negative_moves(game)

    return x_data_positive, x_data_negative


#55436229 999027 999828
def convert_all_games():
    #director_path = Path(r'C:\Users\Jonah Benton\Downloads\9k\9k')
    director_path = Path(r'C:\Users\Jonah Benton\Downloads\8k2\8d')

    #x_positive_file=r'C:\Users\Jonah Benton\GO_trainig_data\test_x_positive.npy'
    #x_negative_file=r'C:\Users\Jonah Benton\GO_trainig_data\test_x_negative.npy'
    #1000000
    #x_data_positive = np.empty((1000000, 19, 19, 5), dtype=np.uint8)
    #x_data_positive.tofile(x_positive_file)

    #x_data_negative = np.empty((5000000, 19, 19, 5), dtype=np.uint8)
    #x_data_negative.tofile(x_negative_file)

    #x_file = r'C:\Users\Jonah Benton\GO_trainig_data\test_x.npy'
    #y_file = r'C:\Users\Jonah Benton\GO_trainig_data\test_y.npy'

    x_file = r'C:\Users\Jonah Benton\GO_trainig_data\test_x_testSet.npy'
    y_file = r'C:\Users\Jonah Benton\GO_trainig_data\test_y_testSet.npy'

    #x_data_positive = np.empty((6000000, 19, 19, 5), dtype=np.uint8)


    #x = np.empty((210000, 19,19,4), dtype=np.uint8)
    #x = np.zeros((1000000, 19, 19, 4), dtype=np.uint8)
    x = np.zeros((1000000, 19, 19, 4), dtype=np.uint8)
    x.tofile(x_file)

    #y = np.zeros((1000000,), dtype=np.uint16)
    y = np.zeros((1000000,), dtype=np.uint16)
    y.tofile(y_file)


    #x = np.memmap(x_file, dtype=np.uint8, mode='r+', shape=(1000000, 19, 19, 4))
    #y = np.memmap(y_file, dtype=np.uint16, mode='r+', shape=(1000000,))
    x = np.memmap(x_file, dtype=np.uint8, mode='r+', shape=(1000000, 19, 19, 4))
    y = np.memmap(y_file, dtype=np.uint16, mode='r+', shape=(1000000,))

    #x_negative = np.memmap(x_negative_file, dtype=np.uint8, mode='r+', shape=(5000000, 19, 19, 5))
    #y = np.empty((210000,), dtype=np.uint16)
    #y = np.memmap(y_file, dtype=np.uint16, mode='r+', shape=(1000000,))

    total_errors=0
    total_frames=0

    for index, file_path in enumerate(director_path.iterdir()):
        game = sgf.load(str(file_path), ignore_illegal_properties=True, fix_file_format=True, disable_warnings=True)
        sequence = game.get_default_sequence()
        current_frames=len(sequence)

        try:
            #input_data = convert_board_state_to_numpy(game)
            #target_data = convert_move_numpy(game)
            x[total_frames:total_frames+current_frames] = convert_board_state_to_numpy(game)
            y[total_frames:total_frames+current_frames] = convert_move_numpy(game)
            total_frames += current_frames
        except sente.exceptions.IllegalMoveException:
            total_errors+=1
        except ValueError as e:
            print(e)
            break
        if index%10==0:
            print(index)

        if total_frames>999000:
            print(f'{total_errors}\n{total_frames}')
            print(x.shape)
            print(y.shape)


            x.flush()
            y.flush()
            break



#game = sgf.load(r'C:\Users\Jonah Benton\Downloads\9k\9k\1387357472019999734.sgf', ignore_illegal_properties=True, fix_file_format=True, disable_warnings=True)
#game.advance_to_root()
#np.set_printoptions(threshold=sys.maxsize)
#print(convert_board_state_to_numpy(game).shape)
#print(convert_move_numpy(game).shape)
#game.advance_to_root()
#seq = game.get_default_sequence()
#game.play(seq[0])
#game.play(seq[1])
#game.play(seq[2])
#print(game)
convert_all_games()




