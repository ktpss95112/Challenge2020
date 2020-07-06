class EventManager:
    '''
    We coordinate communication between the Model, View, and Controller.
    '''
    def __init__(self):
        self.listeners = []

    def register_listener(self, listener):
        '''
        Adds a listener to our spam list.
        It will receive Post()ed events through it's notify(event) call.
        '''
        self.listeners.append(listener)

    def unregister_listener(self, listener):
        '''
        Remove a listener from our spam list.
        This is implemented but hardly used.
        Our weak ref spam list will auto remove any listeners who stop existing.
        '''
        pass

    def post(self, event):
        '''
        Post a new event to the message queue.
        It will be broadcast to all listeners.
        '''
        # # this segment use to debug
        # if not (isinstance(event, Event_EveryTick) or isinstance(event, Event_EverySec)):
        #     print( str(event) )
        for listener in self.listeners:
            listener.notify(event)


class BaseEvent:
    '''
    A superclass for any events that might be generated by
    an object and sent to the EventManager.
    '''
    name = 'Generic event'
    def __init__(self):
        pass

    def __str__(self):
        return self.name


class EventInitialize(BaseEvent):
    name = 'Initialize event'
    '''
    initialize and model stage change to STATE_MENU
    '''

class EventPlay(BaseEvent):
    name = 'GamePlay event'
    '''
    game play and model stage change to STATE_PLAY
    '''


class EventStop(BaseEvent):
    name = 'GameStop event'
    '''
    game stop and model stage change to STATE_STOP
    '''


class EventContinue(BaseEvent):
    name = 'GameContinue event'
    '''
    game continue and model stage change to STATE_PLAY
    '''


class EventRestart(BaseEvent):
    name = 'GameRestart event'
    '''
    game restart and model stage change to STATE_MENU
    '''


class EventTimesUp(BaseEvent):
    name = "Time's Up event"


class EventQuit(BaseEvent):
    name = 'Quit event'


class EventEveryTick(BaseEvent):
    name = 'Tick event'


class EventPlayerMove(BaseEvent):
    name = 'PlayerMove event'

    def __init__(self, player_id, direction):
        self.player_id = player_id
        self.direction = direction

    def __str__(self):
        return f'{self.name} => player_id {self.player_id} move {self.direction}'


class EventPlayerJump(BaseEvent):
    name = 'PlayerJump event'

    def __init__(self, player_id):
        self.player_id = player_id

    def __str__(self):
        return f'{self.name} => player_id {self.player_id} jump'

class EventPlayerAttack(BaseEvent):
    name = 'PlayerAttack event'

    def __init__(self, player_id):
        self.player_id = player_id

    def __str__(self):
        return f'{self.name} => player_id {self.player_id} attack'

class EventPlayerRespawn(BaseEvent):
    name = 'PlayerRespawn event'

    def __init__(self, player_id):
        self.player_id = player_id

    def __str__(self):
        return f'{self.name} => player_id {self.player_id} respawn'


class EventPlayerDied(BaseEvent):
    name = 'PlayerDied event'

    def __init__(self, player_id):
        self.player_id = player_id

    def __str__(self):
        return f'{self.name} => player_id {self.player_id} died'


class EventPlayerItem(BaseEvent):
    name = 'Player press item button (contoller => model)'

    def __init__(self, player_id):
        self.player_id = player_id

    def __str__(self):
        return f'{self.name} => player_id {self.player_id}'


class EventPlayerUseItem(BaseEvent):
    name = 'Player use item event (model => view)'

    def __init__(self, player_id, item_id):
        self.player_id = player_id
        self.item_id = item_id
    def __str__(self):
        return f'{self.name} => player_id {self.player_id} use item {self.item_id}'

    
class EventPlayerPickItem(BaseEvent):
    name = 'Player pick item event (model => view)'

    def __init__(self, player_id, item):
        self.player_id = player_id
        self.item = item # reference to item

    def __str__(self):
        return f'{self.name} => player_id {self.player_id} pick item {self.item_id}'


class EventToggleFullScreen(BaseEvent):
    name = 'ToggleFullScreen event'


class EventBombExplode(BaseEvent):
    name = 'BombExplode event'

    def __init__(self, position):
        self.position = position
