import unittest
import numpy as np
from sente import sgf
from model_handler import AIHandler

game = sgf.load(r'C:\Users\Jonah Benton\Downloads\8k2\8d\1450096422019999389.sgf',ignore_illegal_properties=True, fix_file_format=True, disable_warnings=True)
sequence = game.get_default_sequence()

model = AIHandler('Go_Model_8d.pth')

class TestModelHandler(unittest.TestCase):
    def test_infer_distribution(self):
        game.advance_to_root()
        game.play_sequence(sequence[:25])

        self.assertEqual(len(model.infer_distubution(game)), 361)

    def test_infer_move(self):
        game.advance_to_root()
        game.play_sequence(sequence[:25])
        move = model.infer_best_move(game, 25)
        self.assertGreater(move[0], -1)
        self.assertGreater(move[1], -1)

        self.assertLess(move[0], 19)
        self.assertLess(move[1], 19)

        self.assertTrue(game.is_legal(move[0], move[1]))

        game.play_sequence(sequence[25:len(sequence)])
        move = model.infer_best_move(game, len(sequence))
        print(game.get_winner())
        print(len(sequence))
        self.assertEqual(move, 'pass')

    def test_move_rating(self,):
        distribution = np.array([238, 17, 82, 93, 100, 38, 79, 26])
        move = (0, 17)
        self.assertEqual(model.find_rank_in_distribution(distribution, move), 1)
        move = (1, 7)
        self.assertEqual(model.find_rank_in_distribution(distribution, move), 7)
        move = (4, 17)
        self.assertEqual(model.find_rank_in_distribution(distribution, move), 3)
        move = (3, 2)
        self.assertEqual(model.find_rank_in_distribution(distribution, move), 7)

        random_dist = np.arange(1, 362, )
        rng = np.random.default_rng(seed=42)
        rng.shuffle(random_dist) #208 #7 # 206 # 353
        move = (10, 18)
        self.assertEqual(model.rate_move(random_dist, move), 'Excellent')
        move = (0, 7)
        self.assertEqual(model.rate_move(random_dist, move), 'Blunder')
        move = (10, 16)
        self.assertEqual(model.rate_move(random_dist, move), 'Blunder')
        move = (18, 11)
        self.assertEqual(model.rate_move(random_dist, move), 'Mediocre')
