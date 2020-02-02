import random

class Board:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
    
    def determine_attacker(self):
        if self.player1.num_minions > self.player2.num_minions:
            return self.player1
        elif self.player2.num_minions > self.player1.num_minions:
            return self.player2
        randint = random.randint(0, 1)
        if randint:
            return self.player1
        return self.player2
