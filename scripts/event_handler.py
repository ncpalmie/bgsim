import enum
import random
from hero import Hero
from player import Player

class State(enum.Enum):
    game_start = 0
    tavern_start = 1
    tavern_planning = 2
    tavern_end = 3
    combat_start = 4
    combat = 5
    combat_end = 6
    game_end = 7

class Event:
    def __init__(self, act_state, target, subtargets, actions):
        self.act_state = act_state
        self.target = target
        self.subtargets = subtargets
        self.actions = actions

class EventHandler:
    def __init__(self):
        self.events = {}
        for _state in State:
            self.events[_state.value] = []
        self.state = State.game_start

    def enter_next_state(self):
        self.state += 1
    
    def perform_next_event(self):
        event_list = self.events[self.state]
        while len(event_list) > 0:
            #Continue after minions are done
            pass
        
def setup_human_players(num_humans):
    for player_num in range(num_humans):
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
    
        new_player = Player('HuPlayer_' + str(Player.p_id), 
         Hero.hero_dict[hero_choices[chosen_index]])
        Player.player_dict[new_player.id] = new_player
    
def setup_ai_players(num_ai):
    for i in range(num_ai):
        hero_index = random.randint(0, len(Hero.valid_hero_dbfs) - 1)
        hero_dbf = Hero.valid_hero_dbfs[hero_index]
        Hero.taken_hero_dbfs.append(hero_dbf)
        del Hero.valid_hero_dbfs[hero_index]
        new_player = Player('AIPlayer_' + str(Player.p_id), Hero.hero_dict[hero_dbf])
        Player.player_dict[new_player.id] = new_player

def get_allowed_opps(player_id, players_assigned):
    player = Player.player_dict[player_id]
    player_ids = set(Player.player_dict.keys())
    return player_ids - (set(player.prev_opps) | players_assigned)
    
def check_match_valid(opp_id, players_assigned):
    player_ids = Player.player_dict.keys()
    players_assigned.add(opp_id)
    unpaired_opps = set(player_ids) - players_assigned
    for opp in unpaired_opps:
        if len(get_allowed_opps(opp, players_assigned)) == 0:
            players_assigned.remove(opp_id)
            return False
    return True
    

def setup_next_opponents():
    players_assigned = set()
    player_ids = Player.player_dict.keys()
    for player_id in player_ids:
        if player_id in players_assigned:
            continue
        players_assigned.add(player_id)
        allowed_opps = get_allowed_opps(player_id, players_assigned)
        for opp_id in allowed_opps:
            if check_match_valid(opp_id, players_assigned):
                player = Player.player_dict[player_id]
                opp = Player.player_dict[opp_id]
                player.prev_opps.insert(0, opp_id)
                opp.prev_opps.insert(0, player_id)
                del player.prev_opps[-1]
                del opp.prev_opps[-1]
                player.next_opp = opp_id
                opp.next_opp = player_id
                break
        

        
        
        
