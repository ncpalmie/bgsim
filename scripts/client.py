import ray
from ai import Basic_AI
from hero import Hero
from player import Player

@ray.remote
def Client(object):
    c_id = 0
    def __init__(self, ai):
        self.ai = ai
        self.id = Client.c_id
        self.player = None
        self.id = None

        Client.c_id += 1
        if self.ai:
            self.ai_logic = Basic_AI()

    def select_hero(self):
        hero_choices = Hero.pull_heroes(3)
        if self.ai:
            hero_choice = self.ai_logic.choose_hero(hero_choices)
        else: 
            for i, dbf_id in enumerate(hero_choices):
                print(str(i) + ': ' + Hero.hero_dict[dbf_id].name)
            print('Enter number of hero you want to play: ')
            hero_choice = hero_choices[int(input())]
        return hero_choice

    def initiate_player(self):
        hero_dbf = self.select_hero()
        if self.ai:
            self.player = Player('AIPlayer_' + str(Player.p_id), Hero.hero_dict[hero_dbf])
        else:
            self.player = Player('HuPlayer_' + str(Player.p_id), Hero.hero_dict[hero_dbf])
        self.id = self.player.id
        return self.player            
