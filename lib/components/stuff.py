# -*- coding: utf-8 -*-
# Author  : liyanpeng
# Email   : yanpeng.li@cumt.edu.cn
# Datetime: 2024/10/5 22:05
# Filename: stuff.py
import pygame


class MapItem(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, name):
        super().__init__()
        self.image = pygame.Surface((w, h)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name


