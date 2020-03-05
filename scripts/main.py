import random, sys, time
import constant
import ray
from player import Player
from controllers import EventHandler
from minion import Minion
from hero import Hero, HeroPower

Minion.load_minions()
HeroPower.load_hero_powers()
Hero.load_heroes()
ray.init()

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

state_args = []
event_handler = EventHandler()
state_args.append(num_humans)
state_args.append(num_players - num_humans)

event_handler.run_state(state_args)
event_handler.enter_next_state()
while True:
    event_handler.run_state()
    event_handler.enter_next_state()
    if event_handler.state.value == 3:
        print('TAVERN END ' + str(time.time() - event_handler.debug_time)[:6])
        for player in event_handler.players.values():
            print(player.hand)
        sys.exit()

