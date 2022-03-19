import os
import json

import pygame
from lib.components.info import Info
from lib.init import IMAGEDICT, SCREEN
from lib.constants import *
from lib.components.player import Player


class Level(object):
    def __init__(self):
        self.finish_flag = False
        self.next_state = None

        self.info = Info(state_str='level')
        self.load_map_data()
        self.setup_start_position()
        self.setup_background()
        self.setup_player()

    def load_map_data(self):
        file_name = 'level_1.json'
        file_path = 'resources/json_data/maps'
        with open(os.path.join(file_path, file_name), 'r') as f:
            self.map_data = json.load(f)

    def setup_start_position(self):
        self.position_list = []
        for data in self.map_data['maps']:
            self.position_list.append((data['start_x'], data['end_x'], data['player_x'], data['player_y']))

        self.start_x, self.end_x, self.player_x, self.player_y = self.position_list[0]

    def setup_background(self):
        # level_1
        self.image_name = self.map_data['image_name']
        self.background = IMAGEDICT[self.image_name]
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * SCALE),
                                                                   int(rect.height * SCALE)))
        self.game_window = SCREEN.get_rect()
        self.background_rect = self.background.get_rect()
        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))

    def setup_player(self):
        self.player = Player(name='mario')
        # self.player.rect.x = 300
        # self.player.rect.y = 494
        self.player.rect.x = self.game_window.x + self.player_x
        self.player.rect.bottom = self.player_y

    def update_position(self):
        self.player.rect.x += self.player.x_speed
        self.player.rect.y += self.player.y_speed
        # set range
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x

    def update_window(self):
        window_third = self.game_window.x + self.game_window.width / 3
        if self.player.x_speed > 0 and self.player.rect.centerx > window_third and self.game_window.right < self.end_x:
            self.game_window.x += self.player.x_speed
            # set range
            self.start_x = self.game_window.x

    def update(self, surface, keys):
        self.draw(surface)

        self.player.update(keys=keys)
        self.update_position()
        self.update_window()

    def draw(self, surface):
        # put game_window to background's (0, 0)
        # surface.blit(self.background, (0, 0), self.game_window)
        # surface.blit(self.player.mario_img, self.player.rect)
        self.game_ground.blit(self.background, self.game_window, self.game_window)
        self.game_ground.blit(self.player.mario_img, self.player.rect)
        surface.blit(self.game_ground, (0, 0), self.game_window)
        self.info.draw(surface)
        self.info.update()

