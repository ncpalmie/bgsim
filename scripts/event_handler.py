import enum

class State(enum.Enum):
    game_start = 0
    in_tavern = 1
    exit_tavern = 2
    enter_combat = 3
    in_combat = 4
    exit_combat = 5
    game_end = 6

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
        
