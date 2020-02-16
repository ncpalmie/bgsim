import random
import constant
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

for player in Player.players.values():
    print(player)

#kelth = Player('KTPlayer_' + str(Player.p_id), Hero.hero_dict[constant.KELTHUZAD_ID])
kelth_id = -1

print('===========================')
print('Press enter to iterate one fight...')
while(True):
    kill_num = input()
    if len(kill_num) > 0:
        kill_num = int(kill_num)
        del Player.players[kill_num]
        if Player.players.get(-1, None) == None and len(Player.players.keys()) % 2 != 0:
            Player.players[-1] = Player.kelthuzad
        else:
            del Player.players[-1]
    events.setup_next_opponents()
    for player in Player.players.values():
        print_str = player.name + ' fights with ' + Player.players[player.next_opp].name
        print_str += ' | ' + str(player.prev_opps)
        if not player.next_opp in player.prev_opps[1:]:
            print_str += ' | CORRECT'
        else:
            print_str += ' | INCORRECT'
        print(print_str)

event_handler = EventHandler()

