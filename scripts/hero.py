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
    hero_dict = {}
    valid_hero_dbfs = []
    taken_hero_dbfs = []
    def __init__(self, dbf_id, health, m_id, name, hp_dbf_id):
        self.dbf_id = dbf_id
        self.health = int(health)
        self.id = m_id
        self.name = name
        self.hp_dbf_id = hp_dbf_id

    def __repr__(self):
        return self.name + ' | ' + str(self.dbf_id)
        
    def create_hero(dct):
        return Hero(dct.get('dbfId', None), dct.get('health', None), 
         dct.get('id', None), dct.get('name', None), dct.get('hp_dbf_id', None))

    def setup_valid_heros():
        for hero in Hero.hero_dict.values():
            if hero.name != 'Kel\'Thuzad':
                Hero.valid_hero_dbfs.append(hero.dbf_id)

    def load_heros():
        hero_list = []
        json_file = open('../config/bg_heros.json', 'r')
        json_text = json_file.read().strip()
        json_file.close()
        json_lines = json_text[2:-2].split('},{')
        for line in json_lines:
            new_hero = json.loads('{' + line + '}', object_hook=Hero.create_hero)
            Hero.hero_dict[new_hero.dbf_id] = new_hero
        Hero.setup_valid_heros()

    def pull_heroes(num_heroes):
        hero_dbfs = []
        for i in range(num_heroes):
            new_dbf = valid_hero_dbfs[random.randint(0, len(valid_hero_dbfs)) - 1]
            hero_dbfs.append(new_dbf)
            taken_hero_dbfs.append(new_dbf)
            valid_hero_dbfs.remove(new_dbf)
        return hero_dbfs
