import random
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

event_handler = EventHandler()
event_handler.setup_players(num_humans, num_players - num_humans)

for player in event_handler.players.values():
    print(player)



