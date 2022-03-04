import pygame
from lib.utils import load_img
from lib.init import IMAGEDICT
from lib.constants import *


class TwinklingCoin(pygame.sprite.Sprite):
    def __init__(self):
        super(TwinklingCoin, self).__init__()

        self.coin_surface = []
        self.coin_index = 0
        self.coin_size = (5, 8)
        self.loc = [(1, 160), (9, 160), (17, 160)]
        self.menu_loc = (280, 65)
        self.timer = 0

        self.load_coin()
        self.coin_img = self.coin_surface[self.coin_index]

    def load_coin(self):
        coin_img = IMAGEDICT['item_objects']
        for p in self.loc:
            self.coin_surface.append(load_img(coin_img, p, self.coin_size, (0, 0, 0), SCALE))

    def update(self, *args, **kwargs):
        self.current_time = pygame.time.get_ticks()
        time_interval = [300, 300, 300]

        if self.timer == 0:
            self.timer = self.current_time
        elif (self.current_time - self.timer) > time_interval[self.coin_index]:
            self.coin_index += 1
            self.coin_index %= 3
            self.timer = self.current_time

        self.coin_img = self.coin_surface[self.coin_index]
