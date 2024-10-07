# -*- coding: utf-8 -*-
# Author  : liyanpeng
# Email   : yanpeng.li@cumt.edu.cn
# Datetime: 2022/5/1 22:10
# Filename: init.py
import pygame

from lib.utils import get_imgs
from lib.config import SCREEN_WIDTH, SCREEN_HEIGHT, IMAGE_PATH


pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SuperMario')

IMAGE_DICT = get_imgs(IMAGE_PATH)
