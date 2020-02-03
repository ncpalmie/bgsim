import board
import player
import hero
from minion import Minion

Minion.load_minions()
for key in Minion.minion_dict.keys():
    print(Minion.minion_dict[key])
