import enum

class Event_Type(enum.Enum):
    buy = 0
    sell = 1
    play = 2

class Event:
    e_id = 0
    def __init__(self, ev_type, target, on_player=None, subtargets=None, actions=None):
        self.e_id = Event.e_id
        self.event_type = ev_type
        self.target = target
        self.subtargets = subtargets
        self.actions = actions
        self.on_player = on_player
        Event.e_id += 1

    def __repr__(self):
        return str(self.event_type) + ' : ' + str(self.target)

    def __eq__(self, other):
        if other == None or self == None:
            return False
        return self.e_id == other.e_id
