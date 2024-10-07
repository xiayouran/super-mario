# -*- coding: utf-8 -*-
# Author  : liyanpeng
# Email   : yanpeng.li@cumt.edu.cn
# Datetime: 2022/5/1 22:11
# Filename: level.py
import os
import json
import pygame

from lib.init import IMAGE_DICT, SCREEN
from lib.config import SCALE
from lib.components.info import GameInfo
from lib.components.player import Player
from lib.components.stuff import MapItem
from lib.components.brick import Brick
from lib.components.reward import RewardBox
from lib.components.enemy import Goomba, Koopa


class Level(object):
    def __init__(self):
        self.game_info = {}

    def reset(self, game_info: dict):
        self.game_info = game_info
        self.is_finish = False
        self.next_state = 'game_over'
        self.map_data = None
        self.current_time = None
        self.position_list = []
        self.start_x, self.end_x = None, None  # 地图的起始位置与结束位置(x轴)
        self.player_x, self.player_y = None, None  # 玩家位置

        self.info = GameInfo(state_str='level', game_info=self.game_info)

        self.load_map_data()
        self._init_start_position()
        self._init_background()
        self._init_player()
        self._init_ground_items()
        self._init_bricks()
        self._init_reward_boxes()
        self._init_enemies()

    def load_map_data(self):
        file_name = 'level_1.json'
        file_path = 'resources/json_data/maps'
        with open(os.path.join(file_path, file_name), 'r') as f:
            self.map_data = json.load(f)

    def _init_start_position(self):
        for data in self.map_data['maps']:
            self.position_list.append((data['start_x'], data['end_x'], data['player_x'], data['player_y']))

        self.start_x, self.end_x, self.player_x, self.player_y = self.position_list[0]

    def _init_background(self):
        # level_1
        self.image_name = self.map_data['image_name']
        self.background = IMAGE_DICT[self.image_name]
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background,
                                                 (int(rect.width * SCALE), int(rect.height * SCALE)))
        self.game_window = SCREEN.get_rect()
        self.background_rect = self.background.get_rect()
        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))

    def _init_player(self):
        self.player = Player(name='mario')
        # self.player.rect.x = 300
        # self.player.rect.y = 494
        self.player.rect.x = self.game_window.x + self.player_x
        self.player.rect.bottom = self.player_y

    def _init_ground_items(self):
        self.ground_items_group = pygame.sprite.Group()
        for name in ['ground', 'pipe', 'step']:
            for item in self.map_data[name]:
                map_item = MapItem(item['x'], item['y'], item['width'], item['height'], name=name)
                self.ground_items_group.add(map_item)

    def _init_bricks(self):
        self.brick_group = pygame.sprite.Group()

        for brick_data in self.map_data['brick']:
            if 'brick_num' in brick_data:
                # TODO 下水道砖块
                pass
            else:
                brick = Brick(brick_data['x'], brick_data['y'], brick_data['type'])
                self.brick_group.add(brick)

    def _init_reward_boxes(self):
        self.box_group = pygame.sprite.Group()

        for box_data in self.map_data['box']:
            if 'brick_num' in box_data:
                # TODO 下水道砖块
                pass
            else:
                box = RewardBox(box_data['x'], box_data['y'], box_data['type'])
                self.box_group.add(box)

    def _init_enemies(self):
        self.enemy_group_dict = {}
        for enemy_group_data in self.map_data['enemy']:
            group = pygame.sprite.Group()
            for enemy_group_id, enemy_list in enemy_group_data.items():
                for enemy_data in enemy_list:
                    if enemy_data['type'] == 0:
                        enemy_sprite = Goomba(enemy_data['x'], enemy_data['y'], enemy_data['direction'],
                                              'goomba', enemy_data['color'])
                        group.add(enemy_sprite)
                    elif enemy_data['type'] == 1:
                        enemy_sprite = Koopa(enemy_data['x'], enemy_data['y'], enemy_data['direction'],
                                             'koopa', enemy_data['color'])
                        group.add(enemy_sprite)
                self.enemy_group_dict[enemy_group_id] = group

    def update_position(self):
        self.player.rect.x += self.player.x_speed

        # set range
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x

        # check collision
        self.check_x_collision()
        self.player.rect.y += self.player.y_speed
        self.check_y_collision()

    def check_x_collision(self):
        """碰撞检测"""
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        sprite = pygame.sprite.spritecollideany(self.player, check_group)
        if sprite:
            if self.player.rect.x < sprite.rect.x:
                self.player.rect.right = sprite.rect.left
            else:
                self.player.rect.left = sprite.rect.right
            self.player.x_speed = 0

    def check_y_collision(self):
        """碰撞检测"""
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        sprite = pygame.sprite.spritecollideany(self.player, check_group)
        if sprite:
            if self.player.rect.bottom < sprite.rect.bottom:
                self.player.rect.bottom = sprite.rect.top
                self.player.y_speed = 0
                self.player.current_state = 'walk'
            else:
                self.player.rect.top = sprite.rect.bottom
                self.player.y_speed = 7
                self.player.current_state = 'fall'
        if self.player.rect.top < 0:
            self.player.rect.top = 0
            self.player.y_speed = 7
            self.player.current_state = 'fall'

        # 坠落检测
        self.check_fall(self.player)

    def check_fall(self, sprit):
        sprit.rect.y += 1
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        is_collision = pygame.sprite.spritecollideany(sprit, check_group)
        if not is_collision and sprit.current_state != 'jump':
            sprit.current_state = 'fall'
        sprit.rect.y -= 1

    def update_window(self):
        window_third = self.game_window.x + self.game_window.width / 3
        if self.player.x_speed > 0 and self.player.rect.centerx > window_third and self.game_window.right < self.end_x:
            self.game_window.x += self.player.x_speed
            # set range
            self.start_x = self.game_window.x

    def check_is_die(self):
        if self.player.rect.y > SCREEN.get_height():
            self.player.go_die()

    def update_game_info(self):
        if self.player.dead:
            self.game_info['lives'] -= 1

        if self.game_info['lives'] == 0:
            self.next_state = 'game_over'
        else:
            self.next_state = 'load_screen'

    def update(self, surface, keys):
        self.current_time = pygame.time.get_ticks()
        self.player.update(keys=keys)

        if self.player.dead:
            if self.current_time - self.player.death_time > 3000:
                self.is_finish = True
                self.update_game_info()
        else:
            self.update_position()
            self.check_is_die()
            self.update_window()
            self.info.update()
            self.brick_group.update()
            self.box_group.update()
            for enemy_group in self.enemy_group_dict.values():
                enemy_group.update()

        self.draw(surface)

    def draw(self, surface):
        # put game_window to background's (0, 0)
        # surface.blit(self.background, (0, 0), self.game_window)
        # surface.blit(self.player.mario_img, self.player.rect)
        self.game_ground.blit(self.background, self.game_window, self.game_window)
        self.game_ground.blit(self.player.mario_img, self.player.rect)
        self.brick_group.draw(self.game_ground)
        self.box_group.draw(self.game_ground)
        for enemy_group in self.enemy_group_dict.values():
            enemy_group.draw(self.game_ground)
        surface.blit(self.game_ground, (0, 0), self.game_window)
        self.info.draw(surface)
