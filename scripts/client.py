import ray
from ai import Basic_AI
from hero import Hero
from player import Player

@ray.remote
class Client(object):
    def __init__(self, ai, c_id):
        self.ai = ai
        self.id = c_id

        if self.ai:
            self.ai_logic = Basic_AI()

    def select_hero(self, hero_choices):
        if self.ai:
            hero_choice_dbf = self.ai_logic.choose_hero(hero_choices)
        else: 
            for i, hero in enumerate(hero_choices):
                print(str(i) + ': ' + hero.name)
            print('Enter number of hero you want to play: ')
            hero_choice_dbf = hero_choices[int(input())].dbf_id
        return hero_choice_dbf

    def get_id(self):
        return self.id
