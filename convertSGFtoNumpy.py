from pathlib import Path
import numpy as np
import sente
from sente import sgf, stone

# Directory of SGF data and training data
SGF_directory_path = Path(r'C:\Users\Jonah Benton\Downloads\18k2\18k')
training_data_path = Path(r'TrainingData-18k')
# Number of board states to convert to training data
num_frames = 1001000

training_data_path.mkdir(exist_ok=True)

# Converts all moves in a game to target data by converting human move to a single number representing the move location
def convert_move_to_numpy(game):
    game.advance_to_root()
    sequence = game.get_default_sequence()
    all_moves = np.zeros((len(sequence)),dtype=np.uint16)

    for i in range(len(sequence)):
        x = sequence[i].get_x()
        y = sequence[i].get_y()
        game.play(sequence[i])
        all_moves[i]=(y*19)+x

    return all_moves

# Converts all moves in a game to Input data by using Sente's to_numpy function
def convert_board_state_to_numpy(game):
    game.advance_to_root()
    sequence = game.get_default_sequence()
    all_board_states = np.zeros((len(sequence), 19, 19, 4), dtype=np.uint8)
    all_board_states[0, :, :,2]=1 # Fills the first frame with the values found in an empty board

    for i in range(len(sequence)-1):
        game.play(sequence[i])
        board = game.numpy()

        if game.get_active_player() == stone.WHITE: # Flips white and black stones if its white's turn
            board = np.stack([board[..., 1], board[..., 0], board[..., 2], board[..., 3]], axis=2)

        all_board_states[i+1] = board # Adds board array to i+1 because the first index is an empty board

    return all_board_states

# convert a set number of board states to training data
def convert_all_games():

    x_file = rf'{training_data_path}\X_file.npy'
    y_file = rf'{training_data_path}\y_file.npy'

    x = np.zeros((num_frames, 19, 19, 4), dtype=np.uint8)
    x.tofile(x_file)

    y = np.zeros((num_frames,), dtype=np.uint16)
    y.tofile(y_file)

    x = np.memmap(x_file, dtype=np.uint8, mode='r+', shape=(num_frames, 19, 19, 4))
    y = np.memmap(y_file, dtype=np.uint16, mode='r+', shape=(num_frames,))

    total_errors=0
    total_frames=0


    for index, file_path in enumerate(SGF_directory_path.iterdir()):
        # Loads one game from the SGF directory
        try:
            game = sgf.load(str(file_path), ignore_illegal_properties=True, fix_file_format=True, disable_warnings=True)
            sequence = game.get_default_sequence()
            current_frames = len(sequence)
        except sente.exceptions.InvalidSGFException:
            total_errors += 1
            continue

        try: # Fills the Training data frames with the converted data
            x[total_frames:total_frames+current_frames] = convert_board_state_to_numpy(game)
            y[total_frames:total_frames+current_frames] = convert_move_to_numpy(game)
            total_frames += current_frames

        # Some games are not compatible with sente's rule so this track to number of games which cannot be converted
        except sente.exceptions.IllegalMoveException:
            total_errors+=1

        except ValueError as e:
            print(e)
            break

        if index%100==0: # Prints progress updates to the console
            print(f'Converted {index} games')

        if total_frames>num_frames-1000: # Stops loop before the array size limit is reached
            print(f'Total Errors {total_errors}\nTotal Frames {total_frames}')
            x.flush()
            y.flush()
            break
game = sgf.load(r'C:\Users\Jonah Benton\Downloads\8k2\8d\1450096454019999203.sgf', ignore_illegal_properties=True, fix_file_format=True, disable_warnings=True)
game.advance_to_root()
sequence = game.get_default_sequence()
game.play(sequence[0])
print(sequence[0].get_x(), sequence[0].get_y())
print(game)
#convert_all_games()