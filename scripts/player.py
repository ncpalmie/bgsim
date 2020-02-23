from tavern import Tavern

class Player:
    p_id = 0
    def __init__(self, name, hero):
        self.name = name
        self.hero = hero
        
        if self.name[0] == 'H':
            self.is_ai = False
        else:
            self.is_ai = True
        self.coins = 3
        self.health = 0
        self.triples = 0
        self.winstreak = 0
        self.minions = []
        self.num_minions = 0
        self.tavern = Tavern()
        self.prev_opps = [None, None]
        self.next_opp = None
        self.id = Player.p_id
        Player.p_id += 1
    
    def __repr__(self):
        return self.name + ' playing as ' + self.hero.name
    
    def __eq__(self, other):
        if other == None:
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
