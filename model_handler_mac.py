import io
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
        # 1. Read file manually as standard bytes to strip out CUDA device tags
        with open(model_path, 'rb') as f:
            buffer = io.BytesIO(f.read())
        
        # 2. Load the buffer directly into the CPU
        state_dict = torch.load(buffer, map_location='cpu', weights_only=False)
        model.load_state_dict(state_dict)

        # Apply the exact same logic to your secondary model
        with open('Go_model_8d.pth', 'rb') as f:
            buffer_8d = io.BytesIO(f.read())
            
        state_dict_8d = torch.load(buffer_8d, map_location='cpu', weights_only=False)
        best_model.load_state_dict(state_dict_8d)

    def set_main_model(self, model_name):
        state_dict = torch.load(model_name, weights_only=True)
        model.load_state_dict(state_dict)

    def would_suicide(self, history_list, target_x, target_y, player_color):
        """
        Returns True if playing at (target_x, target_y) leaves the group 
        with 0 liberties and does not capture any enemy stones.
        """
        # 1. Reconstruct current active board from your secure list
        board = [[None for _ in range(19)] for _ in range(19)]
        for move_item in history_list:
            # ✨ ADDED CHECK: Ensure coordinates are not None before writing to grid
            if len(move_item) == 3 and move_item[0] is not None:
                board[move_item[0]][move_item[1]] = move_item[2]
                
        # Put the hypothetical stone on the board
        board[target_x][target_y] = player_color
        
        # 2. Trace liberties using Flood Fill
        visited = set()
        liberties = set()
        
        def flood_fill(cx, cy):
            visited.add((cx, cy))
            for nx, ny in [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]:
                if 0 <= nx < 19 and 0 <= ny < 19:
                    if board[nx][ny] is None:
                        liberties.add((nx, ny))
                    elif board[nx][ny] == player_color and (nx, ny) not in visited:
                        flood_fill(nx, ny)
                        
        flood_fill(target_x, target_y)
        
        # If the group has 0 liberties, it's a suicide play!
        return len(liberties) == 0


    # 1. Takes history_list
    def infer_distubution(self, history_list, current_model=model):
        board_list = [[[0.0 for _ in range(4)] for _ in range(19)] for _ in range(19)]

        # 1. Safely populate the grid
        for move_item in history_list:
            # Check if it's a pass or invalid tuple before doing anything else!
            if move_item[0] is None or move_item[1] is None:
                continue
                
            x, y, stone_color = move_item
            
            if 0 <= x < 19 and 0 <= y < 19:
                if stone_color == sente.stone.BLACK:
                    board_list[x][y][0] = 1.0  # Channel 0: Black stones
                elif stone_color == sente.stone.WHITE:
                    board_list[x][y][1] = 1.0  # Channel 1: White stones

        # 2. Build the array (This will now have a perfect uniform shape!)
        board = np.array(board_list, dtype=np.float32)
        print("Total stones detected by sequence loop:", np.sum(board[:, :, :2]))


        # 3. Handle Player Turn without crashing on passes
        current_active_player = sente.stone.BLACK  
        
        if len(history_list) > 0:
            last_move = history_list[-1]
            
            # Check if the last move played was Black or White
            # Using [-1] pulls the color no matter if it's a 2-item or 3-item tuple!
            if last_move[-1] == sente.stone.BLACK:
                current_active_player = sente.stone.WHITE

        # Check the newly determined player turn
        if current_active_player == sente.stone.WHITE: 
            board = np.stack([board[..., 1], board[..., 0], board[..., 2], board[..., 3]], axis=2)


        # Leave your torch tensor logic below untouched...
        board_contiguous = np.ascontiguousarray(board)
        input_data = torch.from_numpy(board_contiguous).permute(2, 0, 1).float().unsqueeze(0)

        with torch.inference_mode():
            output = current_model(input_data)
            dist = torch.topk(output, k=361, dim=1)
            return dist[1].numpy()[0]

    # 2. Pass BOTH history_list (for tensor) AND game (for legality)
    def infer_best_move(self, history_list, game, total_moves=0, current_model=model, exclude_move=None):
        move_dist = self.infer_distubution(history_list, current_model=current_model)
        
        occupied_moves = set()
        for move_item in history_list:
            if move_item != 'pass' and len(move_item) == 3:
                occupied_moves.add((move_item[0], move_item[1]))

        for move in move_dist:
            y = int(move // 19)
            x = int(move - (y * 19))

            if exclude_move and (x, y) == exclude_move:
                continue

            if (x, y) in occupied_moves:
                continue

            # ✨ NEW: Run manual suicide check for Black's turn
            if self.would_suicide(history_list, x, y, sente.stone.BLACK):
                continue

            # Maintain Sente's internal checks for everything else
            if game.is_legal(int(x) + 1, int(y) + 1):
                return int(x), int(y)


    # 3. Takes history_list
    def recommend_move(self, history_list, game, exclude_move=None):
        # 1. Create a fake history copy to trick the AI
        fake_history = history_list.copy()
        
        # 2. Add a fake "White pass" to the end of the list.
        # This tricks the AI into thinking White just played and that it is BLACK's turn!
        fake_history.append((None, None, sente.stone.WHITE))
        
        # 3. Now run the inference on the tricked board state
        return self.infer_best_move(fake_history, game, current_model=best_model, exclude_move=exclude_move)

    def find_rank_in_distribution(self, distribution, move):
        # 1. Zero-index the user's 1-19 input coordinates to match AI
        z_x = move[0] - 1
        z_y = move[1] - 1
        
        # 2. Map coordinates to the flat 1D index (Try flipping x and y if it still rates poorly!)
        translated_move = (z_y * 19) + z_x
        
        index = np.where(distribution == translated_move)
        if index[0].size == 0:
            return distribution.size - 1
        return int(index[0][0])


    def rate_move(self, distribution, move):
        rank = self.find_rank_in_distribution(distribution, move)
        if rank < 6:
            return 'Excellent'
        elif rank < 51:
            return 'Mediocre'
        else:
            return 'Blunder'

    # 4. Takes history_list
    def rate_user_move(self, history_list, move): 
        # Only pass the list to infer_distubution!
        return self.rate_move(self.infer_distubution(history_list), move)


    def create_score_heat_map(self, game):
        board_array = np.zeros((19, 19))
        
        # 1. Manually query Sente for the state of every intersection
        board_obj = game.get_board()
        for x in range(1, 20):
            for y in range(1, 20):
                stone_at = board_obj.get_stone(x, y)
                
                # Assign values manually to bypass game.numpy()
                if stone_at == sente.stone.BLACK:
                    board_array[x-1, y-1] = 1.0
                elif stone_at == sente.stone.WHITE:
                    board_array[x-1, y-1] = -1.0

        heat_map = board_array.copy()

        kernal = np.array([
            [0.0, 0.1, 0.0],
            [0.1, 1, 0.1],
            [0.0, 0.1, 0.0]
        ])

        for i in range(5):
            heat_map = convolve(heat_map, kernal, mode='constant', cval=0.0)
            heat_map[board_array == 1] = 1.0
            heat_map[board_array == -1] = -1.0

        # ✨ MAKE SURE THIS LINE EXISTS AT THE VERY END OF THE FUNCTION:
        return heat_map


    def estimate_score(self, game):
        territory_map = self.create_score_heat_map(game)
        black = np.sum(territory_map > 0.2)
        white = np.sum(territory_map < -0.2)
        return black-white
