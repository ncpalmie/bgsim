import json

class HeroPower(object):
    hp_dict = {}
    def __init__(self, cost, dbf_id, m_id, name, text):
        self.cost = int(cost)
        self.dbf_id = dbf_id
        self.id = m_id
        self.name = name
        self.text = text

        if self.text != None:
            self.text = self.text.replace('\n', ' ').replace('[x]', '')
            self.text = self.text.replace('<b>', '').replace('</b>', '')

    def __repr__(self):
        return self.name + ' | ' + self.text
        
    def create_hero_power(dct):
        return HeroPower(dct.get('cost', None), dct.get('dbfId', None), 
         dct.get('id', None), dct.get('name', None), dct.get('text', None))

    def load_hero_powers():
        hp_list = []
        json_file = open('../config/bg_hero_powers.json', 'r')
        json_text = json_file.read().strip()
        json_file.close()
        json_lines = json_text[2:-2].split('},{')
        for line in json_lines:
            new_hp = json.loads('{' + line + '}', object_hook=HeroPower.create_hero_power)
            HeroPower.hp_dict[new_hp.dbf_id] = new_hp

class Hero:
    hero_dict = None
    def __init__(self, dbf_id, health, m_id, name, power):
        self.name = name
        self.power = power

def parse_heroes():
    pass 
