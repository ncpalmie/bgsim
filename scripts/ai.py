import random

class Basic_AI:
    def __init__(self):
        self.hero_dbf = None

    def choose_hero(dbf_id_list):
        hero_index = random.randint(0, len(dbf_id_list) - 1)
        self.hero_dbf = dbf_id_list[hero_index]
        return dbf_id_list[hero_index]
