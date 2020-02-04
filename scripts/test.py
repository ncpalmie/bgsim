import board
import player
import hero
from minion import Minion

Minion.load_minions()
dbf_id_list = []
for minion in Minion.min_dict.values():
    dbf_id_list.append(minion.dbf_id)
dbf_id_list.sort(key=lambda x: Minion.min_dict[x].tech_level)
for dbf_id in dbf_id_list:
    print("There are " + str(Minion.min_pool.count(dbf_id)) + " " + Minion.min_dict[dbf_id].name + "(s)")
