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
        self.setup_timers()
        self.load_images()

        # self.mario_size = (12, 16)
        # self.loc = [(1, 160), (9, 160), (17, 160)]
        # self.menu_loc = (280, 65)
        self.timer = 0

    def setup_states(self):
        self.live = None
        self.dead = None
        self.big = None
        self.small = None

    def setup_speed(self):
        self.x_speed = 0
        self.y_speed = 0

    def setup_timers(self):
        # walk time
        self.walking_time = 0
        # diga time
        self.transtion_time = 0

    def load_images(self):
        mario_img = IMAGEDICT['mario_bros']
        # self.mario_surface = []
        # self.mario_surface.append(load_img(mario_img, (178, 32), (12, 16), (0, 0, 0), SCALE))

        self.right_img = []
        self.left_img = []
        self.up_img = []
        self.down_img = []

        img_list = [
            (178, 32, 12, 16),
            (80, 32, 15, 16),
            (96, 32, 16, 16),
            (112, 32, 16, 16),
        ]

        for img_rect in img_list:
            right_img = load_img(mario_img, (img_rect[0], img_rect[1]), (img_rect[2], img_rect[3]), (0, 0, 0), SCALE)
            left_img = pygame.transform.flip(right_img, True, True)
            up_img = pygame.transform.rotate(right_img, 90)
            down_img = pygame.transform.rotate(right_img, -90)

            self.right_img.append(right_img)
            self.left_img.append(left_img)
            self.up_img.append(up_img)
            self.down_img.append(down_img)

        self.mario_index = 0
        self.mario_surface = self.right_img
        self.mario_img = self.mario_surface[self.mario_index]
        self.rect = self.mario_img.get_rect()

    def update(self, *args, **kwargs):
        self.current_time = pygame.time.get_ticks()
        keys = kwargs['keys']
        if keys[pygame.K_RIGHT]:
            self.x_speed = 5
            self.y_speed = 0
            self.mario_surface = self.right_img
        if keys[pygame.K_LEFT]:
            self.x_speed = -5
            self.y_speed = 0
            self.mario_surface = self.left_img
        if keys[pygame.K_UP]:
            self.x_speed = 0
            self.y_speed = -5
            self.mario_surface = self.up_img
        if keys[pygame.K_DOWN]:
            self.x_speed = 0
            self.y_speed = 5
            self.mario_surface = self.down_img

        if self.current_time - self.walking_time > 100:
            self.walking_time = self.current_time
            self.mario_index += 1
            self.mario_index %= 4
        self.mario_img = self.mario_surface[self.mario_index]