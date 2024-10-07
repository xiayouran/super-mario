# -*- coding: utf-8 -*-
# Author  : liyanpeng
# Email   : yanpeng.li@cumt.edu.cn
# Datetime: 2024/10/5 22:05
# Filename: reward.py
import pygame

from lib.init import IMAGE_DICT
from lib.config import SCALE, BRICK_SCALE
from lib.utils import load_img


class RewardBox(pygame.sprite.Sprite):
    def __init__(self, x, y, box_type):
        super().__init__()
        self.x = x
        self.y = y
        self.box_type = box_type
        self.box_size = (16, 16)

        # 图标位置
        self.box_rect = [(384, 0), (400, 0), (416, 0), (432, 0)]

        self.box_surface = []
        self.box_index = 0

        self._load_box()
        self.image = self.box_surface[self.box_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def _load_box(self):
        box_img = IMAGE_DICT['tile_set']
        for rect in self.box_rect:
            self.box_surface.append(load_img(box_img, rect, self.box_size, (0, 0, 0), BRICK_SCALE))
