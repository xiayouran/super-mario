import os
import json

import pygame
from lib.constants import *
from lib.init import IMAGEDICT
from lib.utils import load_img


class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super(Player, self).__init__()

        self.name = name
        self.load_data()
        self.setup_states()
        self.setup_speed()
        self.setup_timers()
        self.load_images()

        # self.mario_size = (12, 16)
        # self.loc = [(1, 160), (9, 160), (17, 160)]
        # self.menu_loc = (280, 65)
        self.timer = 0

    def load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('resources/json_data/player', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)

    def setup_states(self):
        self.state = 'stand'
        self.face_right = True
        self.live = None
        self.dead = None
        self.big = None
        self.small = None

    def setup_speed(self):
        speed = self.player_data['speed']
        self.x_speed = 0
        self.y_speed = 0

        self.max_walk_speed = speed['max_walk_speed']
        self.max_run_speed = speed['max_run_speed']
        self.max_y_velocity = speed['max_y_velocity']
        self.walk_accel = speed['walk_accel']
        self.run_accel = speed['run_accel']
        self.turn_accel = speed['turn_accel']
        self.jump_velocity = speed['jump_velocity']

    def setup_timers(self):
        # walk time
        self.walking_time = 0
        # diga time
        self.transtion_time = 0

    def load_images(self):
        mario_img = IMAGEDICT['mario_bros']
        image_frames = self.player_data['image_frames']

        self.right_small_normal_imgs = []
        self.right_big_normal_imgs = []
        self.right_big_fire_imgs = []
        self.left_small_normal_imgs = []
        self.left_big_normal_imgs = []
        self.left_big_fire_imgs = []

        for k, v in image_frames.items():
            for img_rect in v:
                right_img = load_img(mario_img, (img_rect['x'], img_rect['y']), (img_rect['width'], img_rect['height']), (0, 0, 0), SCALE)
                left_img = pygame.transform.flip(right_img, True, False)

                if k == 'right_small_normal':
                    self.right_small_normal_imgs.append(right_img)
                    self.left_small_normal_imgs.append(left_img)
                elif k == 'right_big_normal':
                    self.right_big_normal_imgs.append(right_img)
                    self.left_big_normal_imgs.append(left_img)
                elif k == 'right_big_fire':
                    self.right_big_fire_imgs.append(right_img)
                    self.left_big_fire_imgs.append(left_img)

        self.mario_index = 0
        self.mario_surface = self.right_small_normal_imgs
        self.mario_img = self.mario_surface[self.mario_index]
        self.rect = self.mario_img.get_rect()

    def update(self, *args, **kwargs):
        self.current_time = pygame.time.get_ticks()
        keys = kwargs['keys']
        self.handel_states(keys)
        # if keys[pygame.K_SPACE]:
        #     self.state = 'jump'
        #     self.y_speed = -5
        #
        # if self.state == 'walk':
        #     if self.current_time - self.walking_time > 100:
        #         self.walking_time = self.current_time
        #         self.mario_index += 1
        #         self.mario_index %= 4
        # if self.state == 'jump':
        #     self.mario_index = 4


    def handel_states(self, keys):
        if self.state == 'stand':
            pass
        elif self.state == 'walk':
            pass
        elif self.state == 'jump':
            pass
        elif self.state == 'basketball':
            pass

        if self.face_right:
            self.mario_img = self.right_small_normal_imgs[self.mario_index]
        else:
            self.mario_img = self.left_small_normal_imgs[self.mario_index]

    def stand(self, keys):
        self.mario_index = 0
        self.x_speed = 0
        self.y_speed = 0

        if keys[pygame.K_RIGHT]:
            self.state = 'walk'
            self.face_right = True
        if keys[pygame.K_LEFT]:
            self.state = 'walk'
            self.face_right = False

    def walk(self, keys):
        if self.current_time - self.walking_time > 100:
            if self.mario_index < 3:
                self.mario_index += 1
            else:
                self.mario_index = 1

        if keys[pygame.K_RIGHT]:
            self.face_right = True
            if self.x_speed < 0:
                self.mario_index = 5
            self.x_speed = self.get_speed(self.x_speed, self.run_accel, self.max_walk_speed, is_right=True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_speed > 0:
                self.mario_index = 5
            self.x_speed = self.get_speed(self.x_speed, self.turn_accel, self.max_walk_speed, is_right=False)
        else:
            if self.face_right:
                self.x_speed -= self.walk_accel
                if self.x_speed <= 0:
                    self.x_speed = 0
                    self.state = 'stand'
            else:
                self.x_speed += self.walk_accel
                if self.x_speed >= 0:
                    self.x_speed = 0
                    self.state = 'stand'

    def jump(self, keys):
        pass

    def basketball(self, keys):
        pass

    def get_speed(self, cur_speed, a, max_speed, is_right=True):
        if is_right:
            return min(cur_speed + a, max_speed)
        return max(cur_speed - a, -max_speed)
