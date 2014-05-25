import math
import unittest

from server.glicko import Glicko

class TestGlicko(unittest.TestCase):

    def setUp(self):
        self.glicko = Glicko(1)

    def test_init(self):
        self.assertEqual(self.glicko.max_rd, 350)
        self.assertEqual(self.glicko.min_rd, 30)
        self.assertEqual(self.glicko.c, 1)
        self.assertEqual(self.glicko.q, math.log(10)/400)

    def test_update_player_win(self):
        actual = self.glicko.update_player(1500, 100, 1500, 100, 0, 1)
        self.assertEqual(actual, (1525, 96))

    def test_update_player_loss(self):
        actual = self.glicko.update_player(1500, 100, 1500, 100, 0, 0)
        self.assertEqual(actual, (1474, 96))

    def test_update_player_draw(self):
        actual = self.glicko.update_player(1500, 100, 1500, 100, 0, 0.5)
        self.assertEqual(actual, (1500, 96))

    # RD is chosen to be < min_rd (default 30).
    # RD' should also be 30.
    def test_min_rd(self):
        actual = self.glicko.update_player(1500, 10, 1500, 100, 0, 1)
        self.assertEqual(actual[1], 30)

    # RD is chosen to be > max_rd (default 350).
    # The calculation should still be performed with an RD of 350.
    def test_max_rd(self):
        actual = self.glicko.update_player(1500, 400, 1500, 100, 0, 1)
        self.assertEqual(actual, (1674, 252))

    def test_c_and_t(self):
        self.glicko = Glicko(20)
        actual = self.glicko.update_player(1500, 100, 1500, 100, 60, 1)
        self.assertEqual(actual, (1574, 164))

if __name__ == '__main__':
    unittest.main()
