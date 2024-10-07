# -*- coding: utf-8 -*-
# Author  : liyanpeng
# Email   : yanpeng.li@cumt.edu.cn
# Datetime: 2022/5/1 22:10
# Filename: main.py
from lib.states.main_menu import Main, MainMenu
from lib.states.load_screen import LoadScreen, GameOver
from lib.states.level import Level


if __name__ == '__main__':
    state_dict = {
        'main_menu': MainMenu(),
        'load_screen': LoadScreen(),
        'level': Level(),
        'game_over': GameOver()
    }

    game = Main(state_dict)
    game.run()
