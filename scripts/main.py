import random
from player import Player
from event_handler import EventHandler
from minion import Minion
from hero import Hero, HeroPower

Minion.load_minions()
HeroPower.load_hero_powers()
Hero.load_heros()
players = []

print('Input number of players: ')
num_players = int(input()) - 1
print('All AI game? y/n: ')
if input() == 'y':
    num_humans = 0
    all_ai = True
else:
    all_ai = False
    print('Input number of human players: ')
    num_humans = int(input())

if not all_ai:
    for player_num in range(0, num_humans):
        print('PLAYER ' + str(player_num) + ':')
        hero_choices = []
        for i in range(0, 3):
            hero_index = random.randint(0, len(Hero.valid_hero_dbfs) - 1)
            hero_choices.append(Hero.valid_hero_dbfs[hero_index])
            Hero.taken_hero_dbfs.append(Hero.valid_hero_dbfs[hero_index])
            del Hero.valid_hero_dbfs[hero_index]
        for i, dbf_id in enumerate(hero_choices):
            print(str(i) + ': ' + Hero.hero_dict[dbf_id].name)
        print('Enter number of hero you want to play: ')
        chosen_index = int(input())
    
        players.append(Player('HumanPlayer_' + str(player_num), 
         Hero.hero_dict[hero_choices[chosen_index]]))

for i in range(0, (num_players - num_humans) + 1):
    hero_index = random.randint(0, len(Hero.valid_hero_dbfs) - 1)
    hero_dbf = Hero.valid_hero_dbfs[hero_index]
    Hero.taken_hero_dbfs.append(hero_dbf)
    del Hero.valid_hero_dbfs[hero_index]
    players.append(Player('AIPlayer_' + str(i), Hero.hero_dict[hero_dbf]))

for player in players:
    print(player)

event_handler = EventHandler()

