import random
import time
from event import Event, Event_Type

class Basic_AI:
    def __init__(self):
        self.hero_dbf = None

    def choose_hero(self, hero_list):
        hero_index = random.randint(0, len(hero_list) - 1)
        self.hero_dbf = hero_list[hero_index].dbf_id
        return self.hero_dbf

    def next_tav_event(self, tavern):
        print(str(self.hero_dbf) + 'buying')
        if len(tavern.minions) > 0:
            buy_index = random.randint(0, len(tavern.minions) - 1)
            if buy_index == 1:
                time.sleep(4)
            return Event(Event_Type.buy, buy_index)
