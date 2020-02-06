import json
import constant
import random

class Minion(object):
    min_dict = {}
    gold_min_dict = {}
    min_pool = []
    def __init__(self, attack, card_class, cost, dbfId, health, m_id, mechanics,
     name, race, rarity, m_set, tech_level, text, m_type):
        self.attack = int(attack)
        self.card_class = card_class
        self.cost = int(cost)
        self.dbf_id = dbfId
        self.health = int(health)
        self.id = m_id
        self.mechanics = mechanics
        self.name = name
        self.race = race
        self.rarity = rarity
        self.set = m_set 
        self.tech_level = int(tech_level)
        self.text = text
        self.type = m_type
        self.golden = False

        if self.text != None:
            self.text = self.text.replace('\n', ' ')

    def __repr__(self):
        ret_string = ""
        ret_string += self.name + ' | ' + str(self.tech_level) 
        ret_string += ' | ' + str(self.text)
        return ret_string
        
    def create_minion(dct):
        return Minion(dct.get('attack', None), dct.get('cardClass', None), 
         dct.get('cost', None), dct.get('dbfId', None), dct.get('health', None), 
         dct.get('id', None), dct.get('mechanics', None), dct.get('name', None),
         dct.get('race', None), dct.get('rarity', None), dct.get('set', None), 
         dct.get('techLevel', None), dct.get('text', None), 
         dct.get('type', None))

    def load_minions():
        minion_list = []
        json_file = open('../config/cards.json', 'r')
        json_text = json_file.read()
        json_file.close()
        json_lines = json_text[2:-3].split('},{')
        for line in json_lines:
            if('techLevel' in line):
                new_minion = json.loads('{' + line + '}', object_hook=Minion.create_minion)
                minion_list.append(new_minion)
        for minion in minion_list:
            if Minion.min_dict.get(minion.dbf_id, None) == None:
                Minion.min_dict[minion.dbf_id] = minion
            elif Minion.min_dict[minion.dbf_id].attack > minion.attack:
                Minion.min_dict[minion.dbf_id].golden = True
                Minion.gold_min_dict[minion.dbf_id] = Minion.min_dict[minion.dbf_id]
                Minion.min_dict[minion.dbf_id] = minion
            else:
                Minion.gold_min_dict[minion.dbf_id] = minion
        Minion.create_minion_pool()        

    def create_minion_pool():
        for minion in sorted(Minion.min_dict.values(), key=lambda x: x.tech_level):
            if minion.tech_level == 1:
                Minion.min_pool.extend([minion.dbf_id] * constant.TIER_1_COPIES)
            elif minion.tech_level == 2:
                Minion.min_pool.extend([minion.dbf_id] * constant.TIER_2_COPIES)
            elif minion.tech_level == 3:
                Minion.min_pool.extend([minion.dbf_id] * constant.TIER_3_COPIES)
            elif minion.tech_level == 4:
                Minion.min_pool.extend([minion.dbf_id] * constant.TIER_4_COPIES)
            elif minion.tech_level == 5:
                Minion.min_pool.extend([minion.dbf_id] * constant.TIER_5_COPIES)
            elif minion.tech_level == 6:
                Minion.min_pool.extend([minion.dbf_id] * constant.TIER_6_COPIES)

def get_rand_minion(max_tier):
    if max_tier == 1:
        return Minion.min_dict[Minion.min_pool[random.randint(0, constant.TIER_1_TOTAL)]]
    elif max_tier == 2:
        return Minion.min_dict[Minion.min_pool[random.randint(0, constant.TIER_1_2_TOTAL)]]
    elif max_tier == 3:
        return Minion.min_dict[Minion.min_pool[random.randint(0, constant.TIER_1_3_TOTAL)]]
    elif max_tier == 4:
        return Minion.min_dict[Minion.min_pool[random.randint(0, constant.TIER_1_4_TOTAL)]]
    elif max_tier == 5:
        return Minion.min_dict[Minion.min_pool[random.randint(0, constant.TIER_1_5_TOTAL)]]
    else:
        return Minion.min_dict[Minion.min_pool[random.randint(0, constant.TIER_1_6_TOTAL)]]
