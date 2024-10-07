# -*- coding: utf-8 -*-
# Author  : liyanpeng
# Email   : yanpeng.li@cumt.edu.cn
# Datetime: 2022/5/1 22:10
# Filename: load_screen.py
import pygame

from lib.components.info import GameInfo


class LoadScreen(object):
    def __init__(self):
        self.game_info = {}

    def reset(self, game_info: dict):
        self.game_info = game_info
        self.is_finish = False
        self.next_state = 'level'
        self.timer = 0
        self.duration = 3000    # 持续时间

        self.info = GameInfo(state_str='load_screen', game_info=self.game_info)

    def update(self, surface, keys):
        self.draw(surface)

        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif (pygame.time.get_ticks() - self.timer) > self.duration:
            self.is_finish = True
            self.timer = 0

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.info.draw(surface)
        self.info.update()


class GameOver(LoadScreen):
    def __init__(self):
        super().__init__()

    def reset(self, game_info: dict):
        self.game_info = game_info
        self.is_finish = False
        self.next_state = 'main_menu'
        self.timer = 0
        self.duration = 4000

        self.info = GameInfo('game_over', game_info=self.game_info)
