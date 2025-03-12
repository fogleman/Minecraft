from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    INVENTORY = auto()
    GAME_OVER = auto()
    COMMAND_LINE = auto()

class StateMachine:
    def __init__(self, initial_state):
        self.state = initial_state
        self.states = {}

    def add_state(self, state, enter_callback=None, update_callback=None, exit_callback=None):
        self.states[state] = {
            'enter': enter_callback,
            'update': update_callback,
            'exit': exit_callback
        }

    def change_state(self, new_state):
        if self.state in self.states and self.states[self.state]['exit']:
            self.states[self.state]['exit']()

        self.state = new_state

        if self.state in self.states and self.states[self.state]['enter']:
            self.states[self.state]['enter']()

    def update(self, dt):
        if self.state in self.states and self.states[self.state]['update']:
            self.states[self.state]['update'](dt)