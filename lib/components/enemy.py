# -*- coding: utf-8 -*-
# Author  : liyanpeng
# Email   : yanpeng.li@cumt.edu.cn
# Datetime: 2024/10/5 22:05
# Filename: enemy.py
import pygame

from lib.config import SCALE, GRAVITY, ANTI_GRAVITY
from lib.init import IMAGE_DICT
from lib.utils import load_img


class EnemyBase(pygame.sprite.Sprite):
    """蘑菇怪"""
    def __init__(self, x, y, direction, name, rect_list, sprite_size=(16, 16)):
        super().__init__()
        self.direction = direction
        self.name = name
        self.img_index = 0
        self.sprite_size = sprite_size
        self.left_rect_list = []
        self.right_rect_list = []

        self._load_image(rect_list)
        self.rect_list = self.left_rect_list if self.direction == 0 else self.right_rect_list
        self.image = self.rect_list[self.img_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        self.timer = 0

    def _load_image(self, rect_list):
        enemy_img = IMAGE_DICT['enemies']
        for rect in rect_list:
            left_rect = load_img(enemy_img, rect, self.sprite_size, (0, 0, 0), SCALE)
            right_rect = pygame.transform.flip(left_rect, flip_x=True, flip_y=False)
            self.left_rect_list.append(left_rect)
            self.right_rect_list.append(right_rect)

    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer > 125:
            self.img_index = (self.img_index + 1) % 2
            self.image = self.rect_list[self.img_index]
            self.timer = self.current_time


class Goomba(EnemyBase):
    def __init__(self, x, y, direction, name, change_color):
        # 图标位置
        bright_rect = [(0, 16), (16, 16), (32, 16)]
        dark_rect = [(0, 48), (16, 48), (32, 48)]

        if change_color:
            self.goomba_rect = dark_rect
        else:
            self.goomba_rect = bright_rect

        super().__init__(x, y, direction, name, self.goomba_rect)


class Koopa(EnemyBase):
    """乌龟怪"""
    def __init__(self, x, y, direction, name, change_color):
        # 图标位置
        bright_rect = [(96, 9), (112, 9), (160, 9)]
        dark_rect = [(96, 72), (112, 72), (160, 72)]
        sprite_size = (16, 22)

        if change_color:
            self.koopa_rect = dark_rect
        else:
            self.koopa_rect = bright_rect

        super().__init__(x, y, direction, name, self.koopa_rect, sprite_size=sprite_size)
