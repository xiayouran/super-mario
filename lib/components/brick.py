# -*- coding: utf-8 -*-
# Author  : liyanpeng
# Email   : yanpeng.li@cumt.edu.cn
# Datetime: 2024/10/5 22:05
# Filename: brick.py
import pygame

from lib.init import IMAGE_DICT
from lib.config import SCALE, BRICK_SCALE
from lib.utils import load_img


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, brick_type, change_color: bool = False):
        super().__init__()
        self.x = x
        self.y = y
        self.brick_type = brick_type
        self.change_color = change_color
        self.brick_size = (16, 16)

        # 图标位置
        bright_rect = [(16, 0), (48, 0)]
        dark_rect = [(16, 32), (48, 32)]

        if self.change_color:
            self.brick_rect = dark_rect
        else:
            self.brick_rect = bright_rect

        self.brick_surface = []
        self.brick_index = 0

        self._load_brick()
        self.image = self.brick_surface[self.brick_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def _load_brick(self):
        brick_img = IMAGE_DICT['tile_set']
        for rect in self.brick_rect:
            self.brick_surface.append(load_img(brick_img, rect, self.brick_size, (0, 0, 0), BRICK_SCALE))
