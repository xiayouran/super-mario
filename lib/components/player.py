import pygame
from lib.constants import *
from lib.init import IMAGEDICT
from lib.utils import load_img


class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super(Player, self).__init__()

        self.name = name
        self.setup_states()
        self.setup_speed()
        self.setup_time()
        self.load_images()

        self.coin_surface = []
        self.coin_index = 0
        self.coin_size = (5, 8)
        self.loc = [(1, 160), (9, 160), (17, 160)]
        self.menu_loc = (280, 65)
        self.timer = 0

        self.load_images()
        self.coin_img = self.coin_surface[self.coin_index]

    def setup_states(self):
        self.live = None
        self.dead = None
        self.big = None
        self.small = None

    def setup_speed(self):
        self.x_speed = 0
        self.y_speed = 0

    def setup_time(self):
        self.warking_time = 0
        self.transtion_time = 0

    def load_images(self):
        coin_img = IMAGEDICT['item_objects']
        for p in self.loc:
            self.coin_surface.append(load_img(coin_img, p, self.coin_size, (0, 0, 0), SCALE))

    def update(self, *args, **kwargs):
        keys = kwargs['keys']
        if keys[pygame.K_RIGHT]:
            self.x_speed = 5
        elif keys[pygame.K_LEFT]:
            self.x_speed = -5

