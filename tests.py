import unittest
import numpy as np
from sente import sgf
from model_handler import AIHandler

game = sgf.load(r'TestGame.sgf',ignore_illegal_properties=True, fix_file_format=True, disable_warnings=True) # Random game to test on
sequence = game.get_default_sequence()

model = AIHandler('models/Go_Model_8d.pth')

class TestModelHandler(unittest.TestCase):
    def test_infer_distribution(self):
        game.advance_to_root()
        for i in range(len(sequence)):
            game.play(sequence[i])

            inference = model.infer_distribution(game)
            self.assertEqual(len(inference), 361)
            self.assertEqual(inference.dtype, np.int64)


    def test_infer_move(self):

        game.advance_to_root()
        for i in range(len(sequence)):
            game.play(sequence[i])
            move = model.infer_best_move(game, i)
            if isinstance(move, str):
                self.assertIn(move, ['pass', 'resign'])
            else:
                x,y = move

                if isinstance(x, int):
                    self.assertGreater(x, 0)
                    self.assertLess(x, 20)
                else:
                    self.fail()

                if isinstance(y, int):
                    self.assertGreater(x, 0)
                    self.assertLess(x, 20)
                else:
                    self.fail()

                self.assertTrue(game.is_legal(x, y))


    def test_move_rating(self,):
        distribution = np.array([345, 323, 82, 307, 100, 38, 79, 26])
        move = (1, 18)
        self.assertEqual(model.find_rank_in_distribution(distribution, move), 1)
        move = (1, 7)
        self.assertEqual(model.find_rank_in_distribution(distribution, move), 7)
        move = (4, 17)
        self.assertEqual(model.find_rank_in_distribution(distribution, move), 3)
        move = (3, 2)
        self.assertEqual(model.find_rank_in_distribution(distribution, move), 7)

        random_dist = np.arange(0, 361, ) # simulates a real distribution by random shuffling values from 1-361
        rng = np.random.default_rng(seed=42)
        rng.shuffle(random_dist)
        move = (18, 11)
        self.assertEqual(model.rate_move(random_dist, move).split(' ')[0], 'Excellent')
        move = (0, 7)
        self.assertEqual(model.rate_move(random_dist, move).split(' ')[0], 'Blunder')
        move = (10, 16)
        self.assertEqual(model.rate_move(random_dist, move).split(' ')[0], 'Blunder')
        move = (4, 6)
        self.assertEqual(model.rate_move(random_dist, move).split(' ')[0], 'Mediocre')

    def test_multi_models(self):# ensures tests work with all models

        model.set_main_model('models/Go_Model_1k.pth')
        self.test_infer_distribution()
        self.test_infer_move()
        self.test_move_rating()

        model.set_main_model('models/Go_Model_18k.pth')
        self.test_infer_distribution()
        self.test_infer_move()
        self.test_move_rating()
