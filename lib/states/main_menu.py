# -*- coding: utf-8 -*-
# Author  : liyanpeng
# Email   : yanpeng.li@cumt.edu.cn
# Datetime: 2022/5/1 22:10
# Filename: main_menu.py
import sys
import pygame

from lib.init import IMAGE_DICT, SCREEN
from lib.config import SCALE
from lib.utils import load_img
from lib.components.info import GameInfo


class Main(object):
    def __init__(self, state_dict, start_state='main_menu'):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.keys = pygame.key.get_pressed()

        self.state_dict = state_dict
        self.state_obj = self.state_dict[start_state]

    def update(self):
        if self.state_obj.is_finish:
            game_info = self.state_obj.game_info
            next_state = self.state_obj.next_state
            self.state_obj.is_finish = False
            self.state_obj = self.state_dict[next_state]
            self.state_obj.reset(game_info)

        self.state_obj.update(self.screen, self.keys)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                if event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()

            self.update()

            # pygame.display.flip()
            pygame.display.update()
            # set FPS
            self.clock.tick(60)


class MainMenu(object):
    def __init__(self):
        self.game_info = {
            'score': 0,
            'coin': 0,
            'lives': 3,
            'player_state': 'small'
        }
        self.reset(game_info=self.game_info)

    def reset(self, game_info: dict):
        self.background = None  # 背景图
        self.caption = None     # 标题图
        self.player = None      # 玩家图
        self.cursor = None      # 游标图
        self.window_size = SCREEN.get_rect()

        self._init_background()
        self._init_player()
        self._init_cursor()

        self.info = GameInfo(state_str='main_menu', game_info=game_info)

        self.is_finish = False
        self.next_state = 'load_screen'
        self.cursor_state = '1P'

    def _init_background(self):
        self.background = IMAGE_DICT['level_1']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background,
                                                 (int(rect.width * SCALE), int(rect.height * SCALE)))
        self.caption = load_img(IMAGE_DICT['title_screen'], (1, 60), (176, 88), (255, 0, 220), SCALE)

    def _init_player(self):
        self.player = load_img(IMAGE_DICT['mario_bros'], (178, 32), (12, 16), (0, 0, 0), SCALE)

    def _init_cursor(self):
        self.cursor = pygame.sprite.Sprite()
        self.cursor.image = load_img(IMAGE_DICT['item_objects'], (24, 160), (8, 8), (0, 0, 0), SCALE)
        rect = self.cursor.image.get_rect()
        rect.x, rect.y = (220, 360)
        self.cursor.rect = rect

    def reset_game_info(self):
        self.game_info = {
            'score': 0,
            'coin': 0,
            'lives': 3,
            'player_state': 'small'
        }

    def update_cursor(self, keys):
        if keys[pygame.K_UP]:
            self.cursor_state = '1P'
            self.cursor.rect.y = 360
        elif keys[pygame.K_DOWN]:
            self.cursor_state = '2P'
            self.cursor.rect.y = 405
        elif keys[pygame.K_RETURN]:
            self.reset_game_info()
            if self.cursor_state == '1P':
                self.is_finish = True
            elif self.cursor_state == '2P':
                self.is_finish = True

    def update(self, surface, keys):
        self.update_cursor(keys)

        surface.blit(self.background, self.window_size)
        surface.blit(self.caption, (165, 100))
        surface.blit(self.player, (110, 494))
        surface.blit(self.cursor.image, self.cursor.rect)

        self.info.update()
        self.info.draw(surface)
