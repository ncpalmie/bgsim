import random
import time
from event import Event, Event_Type

class HumanLogic:
    def __init__(self):
        self.hero_dbf = None

    def choose_hero(self, hero_choices):
        for i, hero in enumerate(hero_choices):
            print(str(i) + ': ' + hero.name)
        print('Enter number of hero you want to play: ')
        hero_choice_dbf = hero_choices[int(input())].dbf_id
        return hero_choice_dbf

    def is_time_left(end_time):
        if time.time() < end_time:
            return True
        return False

    def next_tav_event(self, tavern, hand, minions, end_time):
        print('TIME LEFT: ' + str(end_time - time.time()) + ' seconds')
        print('====================================')
        print('Minions for sale:')
        for i, minion in enumerate(tavern.minions):
            print(str(i) + ': ' + minion.name)
        if tavern.coins >= tavern.min_cost: 
            print('Buy minion? Enter \'y\' for yes: ')
            if not HumanLogic.is_time_left(end_time):
                return None
            if input().lower() == 'y':
                print('Enter minion number: ')
                if not HumanLogic.is_time_left(end_time):
                    return None
                buy_index = int(input())
                return Event(Event_Type.buy, buy_index)
        print('Not enough coins to play a minion.')
        print('====================================')
        print('Hand:')
        for i, minion in enumerate(hand):
            print(str(i) + ': ' + minion.name)
        if len(minions) <= 7 and len(hand) >= 1:
            print('Play minion? Enter \'y\' for yes: ')
            if not HumanLogic.is_time_left(end_time):
                return None
            if input().lower() == 'y':
                #Play minion to board code
                pass
        print('====================================')
        print('Board:')
        for i, minion in enumerate(minions):
            print(str(i) + ': ' + minion.name)
        if len(minions) >= 1:
            print('Alter board? Enter \'y\' for yes: ')
            if not HumanLogic.is_time_left(end_time):
                return None
            if input().lower() == 'y':
                #Alter board code
                pass
        print('====================================')
        return None
            
            
