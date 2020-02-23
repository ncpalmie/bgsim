import random

class Basic_AI:
    def __init__(self):
        self.hero_dbf = None

    def choose_hero(self, hero_list):
        hero_index = random.randint(0, len(hero_list) - 1)
        self.hero_dbf = hero_list[hero_index].dbf_id
        return self.hero_dbf
