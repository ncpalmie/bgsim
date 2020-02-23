import ray
import constant
import time, math, random, enum
import minion as mn
from client import Client
from hero import Hero
from player import Player
from event import Event, Event_Type
from minion import Minion

class State(enum.Enum):
    game_start = 0
    tavern_start = 1
    tavern_planning = 2
    tavern_end = 3
    combat_start = 4
    combat = 5
    combat_end = 6
    game_end = 7

class EventHandler:
    def __init__(self):
        self.events = {}
        for _state in State:
            self.events[_state.value] = []
        self.state = State.game_start
        self.players = {}
        self.clients = {}
        self.round = 0
        self.kelthuzad = None
        self.matchmaker = None

    def enter_next_state(self):
        self.state = State(self.state.value + 1)
    
    def handle_events(self):
        event_list = self.events[self.state.value]
        while len(event_list) > 0:
            #Continue after minions are done
            event_list.pop(0)
            pass

    def run_state(self, args_list=[]):
        if self.state == State.game_start:
            #Arg 1: Number of human players
            #Arg 2: Number of AI players
            self.setup_players(args_list[0], args_list[1])
        elif self.state == State.tavern_start:
            for player in self.players.values():
                tav = player.tavern
                if tav.frozen:
                    continue
                num_offered = math.ceil(tav.tier / 2) + constant.OFFERED_MINIONS
                for i in range(num_offered):
                    tav.minions.append(mn.get_rand_minion(tav.tier))
        elif self.state == State.tavern_planning:
            self.open_tavern(constant.INITIAL_TIMER + self.round * 5) 
            
        self.handle_events()

    def open_tavern(self, tav_time):
        end_time = time.time() + tav_time
        ray_ids = {}
        for client in self.clients.values():
            c_id = ray.get(client.get_id.remote())
            tavern = self.players[c_id].tavern
            ray_ids[client.use_tavern.remote(tavern, end_time)] = c_id
        while time.time() < end_time:
            ready_results, unready_results = ray.wait(list(ray_ids.keys()))
            for i, result in enumerate(ready_results):
                c_id = ray_ids[result]
                tavern = self.players[c_id].tavern
                del ray_ids[result]
                self.events[self.state.value].append(ray.get(result))
                client = self.clients[c_id]
                ray_ids[client.use_tavern.remote(tavern, end_time)] = c_id

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
        
        
