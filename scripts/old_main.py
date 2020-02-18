import random
import constant
from player import Player
from controllers import EventHandler
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

event_handler = EventHandler()
event_handler.setup_all_players(num_humans, num_players - num_humans)

for player in event_handler.players.values():
    print(player)

#kelth = Player('KTPlayer_' + str(Player.p_id), Hero.hero_dict[constant.KELTHUZAD_ID])
kelth_id = -1

print('===========================')
print('Press enter to iterate one fight...')
while(True):
    kill_num = input()
    if len(kill_num) > 0:
        kill_num = int(kill_num)
        del event_handler.players[kill_num]
        if event_handler.players.get(-1, None) == None and len(event_handler.players.keys()) % 2 != 0:
            event_handler.players[-1] = event_handler.kelthuzad
        else:
            del event_handler.players[-1]
    event_handler.matchmaker.setup_next_opponents()
    for player in event_handler.players.values():
        print_str = player.name + ' fights with ' + event_handler.players[player.next_opp].name
        print_str += ' | ' + str(player.prev_opps)
        if not player.next_opp in player.prev_opps[1:]:
            print_str += ' | CORRECT'
        else:
            print_str += ' | INCORRECT'
        print(print_str)


