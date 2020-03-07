import enum

class Event_Type(enum.Enum):
    buy = 0
    sell = 1
    play = 2

class Event:
    e_id = 0
    def __init__(self, ev_type, target, subtargets=None, on_player=None, actions=None):
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

'''
Example event types:

Buy: 
    Need target as desired minion's index in tavern minions list
    return Event(Event_Type.buy, buy_index) 
Sell:
    Need target as desired minion's index in board minions list
    return Event(Event_Type.sell, sell_index)
Play:
    Need target as desired minion's index in hand card list
    Need subtargets IF there is a desired position on board as index
        of board minion to place to right of (-1 is acceptable for far left)
    Need actions which should be input after event is returned to main client
    return Event(Event_Type.play, hand_index, pos_index)
        THEN ref_event.actions = Minion.get_min_events(hand[hand_index])
'''
