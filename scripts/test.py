import board
import constant
import player
import hero
import minion as mins
from minion import Minion

Minion.load_minions()
dbf_id_list = []
for minion in Minion.min_dict.values():
    dbf_id_list.append(minion.dbf_id)
dbf_id_list.sort(key=lambda x: Minion.min_dict[x].tech_level)
tot = 0
for dbf_id in Minion.min_pool:
    if Minion.min_dict[dbf_id].tech_level == 6:
        print(Minion.min_dict[dbf_id].name + str(Minion.min_dict[dbf_id].attack))
        tot += 1
print("Total: " + str(tot))

temp = int(input())
while temp != -1:
    print("Minion from Tier " + str(temp) + " or lower: " + mins.get_rand_minion(temp).name)
    temp = input()
