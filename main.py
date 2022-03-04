from lib.states.main_menu import Main, MainMenu
from lib.states.load_screen import LoadScreen
from lib.states.level import Level


if __name__ == '__main__':
    state_dict = {
        'main_menu': MainMenu(),
        'load_screen': LoadScreen(),
        'level': Level()
    }

    game = Main(state_dict)
    game.run()
