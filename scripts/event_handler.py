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
    
def find_ideal_opponent(player_id, players_assigned):
    player = Player.player_dict[player_id]
    player_id_set = set(Player.player_dict.keys())
    if player.prev_opponents[1] == None:
        invalid_players = players_assigned | set(player.prev_opponents) 
        valid_players = list(player_id_set - invalid_players)
        return valid_players[random.randint(0, len(valid_players) - 1)]

    unassigned = player_id_set - players_assigned
    if len(unassigned) == 1:
        return list(unassigned)[0] 
    rand_opp_id = random.choice(tuple(unassigned))
    rand_opp_1 = Player.player_dict[rand_opp_id]
    rand_opp_id = random.choice(tuple(unassigned))
    rand_opp_2 = Player.player_dict[rand_opp_id]
    opt_choices = set(rand_opp_1.prev_opponents) | set(rand_opp_2.prev_opponents)
    best_opts = opt_choices - (players_assigned | set(player.prev_opponents))
    if len(best_opts) == 0:
        return random.choice(tuple(player_id_set - (players_assigned | set(player.prev_opponents))))
    else:
        return random.choice(tuple(best_opts))
    

def setup_next_opponents():
    players_assigned = set()
    for player_id in Player.player_dict.keys():
        if not player_id in players_assigned:
            players_assigned.add(player_id)
            opp_id = find_ideal_opponent(player_id, players_assigned)

            #Setup iterated player information
            Player.player_dict[player_id].prev_opponents.insert(0, opp_id)
            del Player.player_dict[player_id].prev_opponents[-1]
            Player.player_dict[player_id].next_opponent = opp_id

            #Setup chosen player information
            Player.player_dict[opp_id].prev_opponents.insert(0, player_id)
            del Player.player_dict[opp_id].prev_opponents[-1]
            Player.player_dict[opp_id].next_opponent = player_id
            
            players_assigned.add(opp_id)
            
        
