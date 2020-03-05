import ray
import time
from ai import Basic_AI
from hero import Hero
from player import Player
from human import HumanLogic
from event import Event, Event_Type

@ray.remote
class Client(object):
    def __init__(self, ai, c_id):
        self.is_ai = ai
        self.id = c_id
        self.events_made = []
        self.in_tavern = False

        if self.is_ai:
            self.logic = Basic_AI()
        else:
            self.logic = HumanLogic()

    def is_time_left(self, end_time):
        if time.time() < end_time:
            return True
        return False

    def use_tavern(self, tavern, end_time, debug_time):
        print('CLIENT ' + str(self.id) + ' RECEIVED TAVERN ' + str(time.time() - debug_time)[:6])
        self.events_made = []
        while len(self.events_made) == 0 and Client.is_time_left(end_time):
            if tavern.coins >= tavern.min_cost:
                ret_event = self.logic.next_tav_event(tavern, end_time)
            else:
                ret_event = None
            if ret_event == None:
                break
            else:
                ret_event.on_player = self.id
                self.events_made.append(ret_event)
        print('CLIENT ' + str(self.id) + ' FINISHED TAVERN ' + str(time.time() - debug_time)[:6])
        return self.events_made
                
    def select_hero(self, hero_choices):
        hero_choice_dbf = self.logic.choose_hero(hero_choices)
        return hero_choice_dbf

    def get_id(self):
        return self.id
