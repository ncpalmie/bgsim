import enum

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
        
