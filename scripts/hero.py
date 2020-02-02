class HeroPower:
    hero_power_dict = None
    def __init__(self, name, desc, is_passive, cost):
        self.name = name
        self.desc = desc
        self.action_function = None
        self.initial_function = None

        if cost == 'None':
            self.cost = None
        else:
            self.cost = int(cost)

        if is_passive == 'true':
            self.is_passive = True
        else:
            self.is_passive = False        
        
    def __repr__(self):
        ret_string = ""
        ret_string += self.name + ' | ' + self.desc + ' | Is passive: '
        ret_string += str(self.is_passive) + ' | Cost: ' + str(self.cost)
        return ret_string

class Hero:
    hero_dict = None
    def __init__(self, name, power):
        self.name = name
        self.power = power

def parse_hero_powers():
    ret_dict = {}
    powers_file = open('../config/hero_powers.txt', 'r')
    powers_lines = powers_file.readlines()
    for power_line in powers_lines:
        arguments = power_line.split(',')
        new_power = HeroPower(arguments[0], arguments[1], arguments[2],
         arguments[4])
        ret_dict[arguments[0]] = new_power
    powers_file.close()
    HeroPower.hero_power_dict = ret_dict

def parse_heroes():
    pass 
