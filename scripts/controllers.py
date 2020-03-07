import ray
import constant
import time, math, random, enum
import minion as mn
from client import Client
from hero import Hero
from player import Player
from event import Event, Event_Type
from minion import Minion
from minion import BoardMinion

class State(enum.Enum):
    game_start = 0
    t_start = 1
    t_plan = 2
    t_end = 3
    c_start = 4
    c_sim = 5
    c_end = 6
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
        self.debug_time = time.time()

    def enter_next_state(self):
        self.state = State(self.state.value + 1)
    
    def handle_events(self):
        event_list = self.events[self.state.value]
        while len(event_list) > 0:
            next_event = event_list.pop(0)
            if next_event.event_type == Event_Type.buy:
                ref_player = self.players[next_event.on_player]
                bought_min = ref_player.tavern.minions.pop(next_event.target)
                ref_player.hand.append(bought_min)
                ref_player.tavern.coins -= ref_player.tavern.min_cost
            if next_event.event_type == Event_Type.play:
                ref_player = self.players[next_event.on_player]
                card = ref_player.hand.pop(next_event.target)
                board_min = BoardMinion(card.attack, card.health, 0, card)
                ref_player.minions.append(board_min)

    def run_state(self, args_list=[]):
        if self.state == State.game_start:
            #Arg 1: Number of human players
            #Arg 2: Number of AI players
            self.setup_players(args_list[0], args_list[1])
        elif self.state == State.t_start:
            for player in self.players.values():
                tav = player.tavern
                if tav.frozen:
                    continue
                num_offered = math.ceil(tav.tier / 2) + constant.OFFERED_MINIONS
                for i in range(num_offered):
                    tav.minions.append(mn.get_rand_minion(tav.tier))
        elif self.state == State.t_plan:
            self.open_tavern(constant.INITIAL_TIMER + self.round * 5) 
            
    def open_tavern(self, tav_time):
        end_time = time.time() + tav_time
        ray_ids = {}
        for client in self.clients.values():
            c_id = ray.get(client.get_id.remote())
            tavern = self.players[c_id].tavern
            hand = self.players[c_id].hand
            minions = self.players[c_id].minions
            #print('OPEN TAVERN SEND NOW TO CLIENT ' + str(c_id) + ' ' + str(time.time() - self.debug_time)[:6])
            ray_ids[client.use_tavern.remote(tavern, hand, minions, end_time, self.debug_time)] = c_id
        while time.time() < end_time:
            if time.time() * 1000 % constant.TAV_REFRESH_RATE != 0:
                continue
            ready_results, unready_results = ray.wait(list(ray_ids.keys()), len(list(ray_ids.keys())))
            for i, result in enumerate(ready_results):
                c_id = ray_ids[result]
                tavern = self.players[c_id].tavern
                hand = self.players[c_id].hand
                minions = self.players[c_id].minions
                del ray_ids[result]
                for event in ray.get(result):
                    if not event in self.events[self.state.value]:
                        self.events[self.state.value].append(event)
                self.handle_events()
                client = self.clients[c_id]
                #print('TAVERN RESEND NOW TO CLIENT ' + str(c_id) + ' ' + str(time.time() - self.debug_time)[:6])
                ray_ids[client.use_tavern.remote(tavern, hand, minions, end_time, self.debug_time)] = c_id

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
        
        
