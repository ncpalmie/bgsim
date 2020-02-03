import json

class Minion(object):
    minion_dict = None 
    def __init__(self, attack, card_class, cost, dbfId, health, m_id, mechanics,
     name, race, rarity, m_set, tech_level, text, m_type):
        self.attack = int(attack)
        self.card_class = card_class
        self.cost = int(cost)
        self.dbfId = dbfId
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
        ret_dict = {}
        json_file = open('../config/cards.json', 'r')
        json_text = json_file.read()
        json_file.close()
        json_lines = json_text[2:-3].split('},{')
        for line in json_lines:
            if(line[1:7] == 'attack' and 'BATTLEGROUNDS' in line):
                new_minion = json.loads('{' + line + '}', object_hook=Minion.create_minion)
                if new_minion.set == 'BATTLEGROUNDS':
                    ret_dict[new_minion.name] = new_minion
        Minion.minion_dict = ret_dict
        
