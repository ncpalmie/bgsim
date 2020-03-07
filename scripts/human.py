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
        print('You have ' + str(tavern.coins) + ' coins left')
        print('====================================')
        print('Minions for sale:')
        for i, minion in enumerate(tavern.minions):
            print(str(i) + ': ' + minion.name)
        print('====================================')
        print('Board:')
        for i, board_minion in enumerate(minions):
            print(str(i) + ': ' + board_minion.minion.name)
        print('====================================')
        print('Hand:')
        for i, minion in enumerate(hand):
            print(str(i) + ': ' + minion.name)
        print('====================================')
        if tavern.coins >= tavern.min_cost: 
            print('Buy minion? Enter \'b\' for yes: ')
            if not HumanLogic.is_time_left(end_time):
                return None
            if input().lower() == 'b':
                print('Enter minion number in tavern: ')
                if not HumanLogic.is_time_left(end_time):
                    return None
                buy_index = int(input())
                return Event(Event_Type.buy, buy_index)
        else:
            print('Not enough coins to buy a minion.')
        if len(minions) >= 1:
            print('Sell minion? Enter \'s\' for yes:')
            if not HumanLogic.is_time_left(end_time):
                return None
            if input().lower() == 's':
                #Play minion to board code
                pass
        else:
            print('No minions to sell.')
        if len(minions) <= 7 and len(hand) >= 1:
            print('Play minion? Enter \'p\' for yes: ')
            if not HumanLogic.is_time_left(end_time):
                return None
            if input().lower() == 'p':
                #Play minion to board code
                print('Enter minion number in hand: ')
                if not HumanLogic.is_time_left(end_time):
                    return None
                play_index = int(input())
                return Event(Event_Type.play, play_index)
        if len(minions) >= 1:
            print('Alter board? Enter \'a\' for yes: ')
            if not HumanLogic.is_time_left(end_time):
                return None
            if input().lower() == 'a':
                #Alter board code
                pass
        print('====================================')
        return None
            
            
