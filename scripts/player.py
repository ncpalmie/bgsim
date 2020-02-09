class Player:
    def __init__(self, name, hero):
        self.name = name
        self.hero = hero
        self.coins = 3
        self.health = 40
        self.triples = 0
        self.winstreak = 0
        self.minions = []
        self.num_minions = 0
        self.tav_tier = 1
        self.prev_opponents = [None, None, None]
    
    def __repr__(self):
        return self.name + ' playing as ' + self.hero.name
