import unittest
from sente import sgf

from model_handler import AI_hanndler

class TestModelHanndler(unittest.TestCase):
    def test_infer_distribution(self):
        game = sgf.load(r'C:\Users\Jonah Benton\Downloads\8k2\8d\1450096422019999389.sgf',ignore_illegal_properties=True, fix_file_format=True, disable_warnings=True)
        sequence = game.get_default_sequence()
        game.play_sequence(sequence[:25])

        model = AI_hanndler()
        self.assertEqual(len(model.infer_distubution(game)), 361)

    def test_infer_move(self):
        game = sgf.load(r'C:\Users\Jonah Benton\Downloads\8k2\8d\1450096422019999389.sgf',ignore_illegal_properties=True, fix_file_format=True, disable_warnings=True)
        sequence = game.get_default_sequence()
        game.play_sequence(sequence[:25])
        model = AI_hanndler()
        move = model.infer_best_move(game)
        self.assertGreater(move[0], -1)
        self.assertGreater(move[1], -1)

        self.assertLess(move[0], 19)
        self.assertLess(move[1], 19)

        self.assertTrue(game.is_legal(move[0], move[1]))



