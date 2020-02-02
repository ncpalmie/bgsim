import unittest
import player, board

class TestSuite(unittest.TestCase):
    def test_board_first_attacker(self):
         player1 = player.Player("p1",
