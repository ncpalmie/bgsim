import ray
import time
from ai import Basic_AI
from hero import Hero
from player import Player
from event import Event, Event_Type

@ray.remote
class Client(object):
    def __init__(self, ai, c_id):
        self.is_ai = ai
        self.id = c_id
        self.events_made = []
        self.in_tavern = False

        if self.is_ai:
            self.ai_logic = Basic_AI()

    def is_time_left(self, end_time):
        if time.time() < end_time:
            return True
        return False

    def use_tavern(self, tavern, end_time):
        self.events_made = []
        while len(self.events_made) == 0 and Client.is_time_left(end_time):
            if self.is_ai:
                self.events_made.append(self.ai_logic.next_tav_event(tavern))
            else:
                print('TIME LEFT: ' + str(end_time - time.time()) + ' seconds')
                print('Minions for sale:')
                for i, minion in enumerate(tavern.minions):
                    print(str(i) + ': ' + minion.name)
                print('Buy minion? Enter \'y\' for yes: ')
                if not Client.is_time_left(end_time):
                    break
                if input().lower() == 'y':
                    print('Enter minion number: ')
                    if not Client.is_time_left(end_time):
                        break
                    buy_index = int(input())
                    self.events_made.append(Event(Event_Type.buy, buy_index))
        return self.events_made
                
    def select_hero(self, hero_choices):
        if self.is_ai:
            hero_choice_dbf = self.ai_logic.choose_hero(hero_choices)
        else: 
            for i, hero in enumerate(hero_choices):
                print(str(i) + ': ' + hero.name)
            print('Enter number of hero you want to play: ')
            hero_choice_dbf = hero_choices[int(input())].dbf_id
        return hero_choice_dbf

    def get_id(self):
        return self.id
