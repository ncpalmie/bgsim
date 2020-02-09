import board
import constant
import player
import hero
import minion as mins
from minion import Minion
from hero import Hero

Hero.load_heros()
for dbf_id in Hero.hero_dict.keys():
    print(Hero.hero_dict[dbf_id])
