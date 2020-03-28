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
        print('Enter \'b\' to buy a minion, \'s\' to sell a minion, \n')
        print('\'p\' to play a minion, \'a\' to alter the board, or \'e\' to end your turn early:')
        if not HumanLogic.is_time_left(end_time):
            return None
        
        choice = input().lower()

        while choice != 'e':
            if choice == 'b':
                return self.buy_action(tavern, end_time)
            if choice == 's':
                return self.sell_action(minions, end_time)
            if choice == 'p':
                return self.play_action(minions, hand, end_time)
            if choice == 'a':
                return self.alter_action(minions, end_time)
            print('Enter \'b\' to buy a minion, \'s\' to sell a minion,')
            print('\'p\' to play a minion, \'a\' to alter the board, or \'e\' to end your turn early:')
            if not HumanLogic.is_time_left(end_time):
                return None
            choice = input().lower()

        return Event(Event_Type.end)
            
    def buy_action(self, tavern, end_time):
        if tavern.coins >= tavern.min_cost: 
            print('Enter minion number in tavern: ')
            if not HumanLogic.is_time_left(end_time):
                return None
            buy_index = int(input())
            return Event(Event_Type.buy, buy_index)
        else:
            print('Not enough coins to buy a minion.')

    def play_action(self, minions, hand, end_time):
        if len(minions) <= 7 and len(hand) >= 1:
            print('Enter minion number in hand: ')
            if not HumanLogic.is_time_left(end_time):
                return None
            play_index = int(input())
            return Event(Event_Type.play, play_index)
        else:
            print ('No cards to play/board space to place a minion.')

    def sell_action(self, minions, end_time):
        if len(minions) >= 1:
            pass
        else:
            print('No minions to sell.')

    def alter_action(self, minions, end_time):
        if len(minions) >= 1:
            pass
        else:
            print('Nothing on board to alter.')
