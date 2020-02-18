import random
import constant
import ray
from player import Player
from controllers import EventHandler
from minion import Minion
from hero import Hero, HeroPower
from client import Client

ray.init()
Minion.load_minions()
HeroPower.load_hero_powers()
Hero.load_heros()

c = Client.remote()
obj_id = c.test.remote()

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
event_handler.setup_clients(num_humans, num_players - num_humans)

for player in event_handler.players.values():
    print(player)


