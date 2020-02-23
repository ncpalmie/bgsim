import enum
import ray
import random
import constant
from client import Client
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
        self.players = {}
        self.clients = {}
        self.kelthuzad = None
        self.matchmaker = None

    def enter_next_state(self):
        self.state += 1
    
    def perform_next_event(self):
        event_list = self.events[self.state]
        while len(event_list) > 0:
            #Continue after minions are done
            pass
    
    def setup_clients(self, num_clients, is_ai):
        for i in range(num_clients):
            client = Client.remote(is_ai, Player.p_id)
            c_id = Player.p_id 
            client_hero = client.select_hero.remote(Hero.pull_heroes(3))
            if is_ai:
                name = 'AIPlayer_' + str(c_id)
            else:
                name = 'HuPlayer_' + str(c_id)
            self.players[c_id] = Player(name, Hero.heroes[ray.get(client_hero)])
            self.clients[c_id] = client

    def setup_players(self, num_humans, num_ai):    
        self.setup_clients(num_humans, False)
        self.setup_clients(num_ai, True)
        self.matchmaker = Matchmaker(self.players)

    def setup_human_players(self, num_humans):
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
            self.players[new_player.id] = new_player
    
    def setup_ai_players(self, num_ai):
        for i in range(num_ai):
            hero_index = random.randint(0, len(Hero.valid_hero_dbfs) - 1)
            hero_dbf = Hero.valid_hero_dbfs[hero_index]
            Hero.taken_hero_dbfs.append(hero_dbf)
            del Hero.valid_hero_dbfs[hero_index]
            new_player = Player('AIPlayer_' + str(Player.p_id), Hero.hero_dict[hero_dbf])
            self.players[new_player.id] = new_player
        #Add Kel'Thuzad to list
        new_player = Player('Kel\'Thuzad', Hero.hero_dict[constant.KELTHUZAD_ID])
        new_player.id = -1
        self.kelthuzad = new_player

class Matchmaker:
    def __init__(self, players):
        self.players = players

    def get_player_opts(self, player_id, players_assigned):
        player_opts = set(self.players.keys())
        invalid_opts = players_assigned | set(self.players[player_id].prev_opps)
        invalid_opts.add(player_id)
        return list(player_opts - invalid_opts)

    def setup_match(self, player_id, opp_id):
        player = self.players[player_id]
        opp = self.players[opp_id]
        player.prev_opps.insert(0, opp_id)
        player.next_opp = opp_id
        opp.prev_opps.insert(0, player_id)
        opp.next_opp = player_id
        del player.prev_opps[-1]
        del opp.prev_opps[-1]

    def setup_next_opponents(self):
        players_assigned = set()
        player_ids = list(self.players.keys())
        if len(player_ids) == 2:
            self.setup_match(player_ids[0], player_ids[1])
            return
        while len(players_assigned) != len(self.players.keys()):
            player_id = sorted(player_ids, key=lambda x: len(self.get_player_opts(x, 
             players_assigned)))[0]
            if player_id in players_assigned:
                player_ids.remove(player_id)
                continue
            player_opts = self.get_player_opts(player_id, players_assigned)
            opp_id = player_opts[random.randint(0, len(player_opts) - 1)]
            self.setup_match(player_id, opp_id)
            players_assigned.add(player_id)
            players_assigned.add(opp_id)
        
        
