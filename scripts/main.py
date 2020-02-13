import random
import event_handler as events
from player import Player
from event_handler import EventHandler
from minion import Minion
from hero import Hero, HeroPower

Minion.load_minions()
HeroPower.load_hero_powers()
Hero.load_heros()

print('Input number of players: ')
num_players = int(input())
print('All AI game? y/n: ')
if input() == 'y':
    num_humans = 0
    all_ai = True
else:
    all_ai = False
    print('Input number of human players: ')
    num_humans = int(input())

if not all_ai:
    events.setup_human_players(num_humans)

events.setup_ai_players(num_players - num_humans)

for player in Player.player_dict.values():
    print(player)

print('===========================')
print('Press enter to iterate one fight...')
while(True):
    input()
    events.setup_next_opponents()
    for player in Player.player_dict.values():
        print_str = player.name + ' fights with ' + Player.player_dict[player.next_opp].name
        print_str += ' | ' + str(player.prev_opps)
        if not player.next_opp in player.prev_opps[1:]:
            print_str += ' | CORRECT'
        else:
            print_str += ' | INCORRECT'
        print(print_str)

event_handler = EventHandler()

