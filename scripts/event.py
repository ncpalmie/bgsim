import enum

class Event_Type(enum.Enum):
    buy = 0
    sell = 1
    play = 2

class Event:
    def __init__(self, ev_type, target, subtargets=None, actions=None):
        self.event_type = ev_type
        self.target = target
        self.subtargets = subtargets
        self.actions = actions
