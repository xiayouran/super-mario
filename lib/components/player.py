# -*- coding: utf-8 -*-
# Author  : liyanpeng
# Email   : yanpeng.li@cumt.edu.cn
# Datetime: 2022/5/1 22:11
# Filename: player.py
import os
import json
import pygame

from lib.config import SCALE, GRAVITY, ANTI_GRAVITY
from lib.init import IMAGE_DICT
from lib.utils import load_img


class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super(Player, self).__init__()

        self.name = name
        self.player_data = None
        self.current_time = None
        self.current_state = None
        self.walking_time = None
        self.death_time = None
        self.max_walk_speed = None
        self.walk_accel = None
        self.mario_img = None
        self.mario_index = 0
        self.x_speed = 0
        self.y_speed = 0
        self.face_right = True
        self.dead = False

        self._load_data()
        self._init_states()
        self._init_speed()
        self._init_timers()
        self._load_images()

        # self.mario_size = (12, 16)
        # self.loc = [(1, 160), (9, 160), (17, 160)]
        # self.menu_loc = (280, 65)
        self.timer = 0

    def _load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('resources/json_data/player', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)

    def _init_states(self):
        self.current_state = 'stand'
        self.face_right = True
        self.live = None
        self.dead = None
        self.big = None
        self.small = None
        self.jump_ok = True

    def _init_speed(self):
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
        self.gravity = GRAVITY
        self.anti_gravity = ANTI_GRAVITY

        self.max_x_speed = self.max_walk_speed
        self.x_accel = self.walk_accel

    def _init_timers(self):
        self.walking_time = 0
        self.transtion_time = 0
        self.death_time = 0

    def _load_images(self):
        mario_img = IMAGE_DICT['mario_bros']
        image_frames = self.player_data['image_frames']

        self.right_small_normal_imgs = []
        self.right_big_normal_imgs = []
        self.right_big_fire_imgs = []
        self.left_small_normal_imgs = []
        self.left_big_normal_imgs = []
        self.left_big_fire_imgs = []

        for k, v in image_frames.items():
            for img_rect in v:
                right_img = load_img(mario_img, (img_rect['x'], img_rect['y']),
                                     (img_rect['width'], img_rect['height']),
                                     (0, 0, 0), SCALE)
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

    def check_jump_is_ok(self, keys):
        if not keys[pygame.K_SPACE]:
            self.jump_ok = True

    def handel_states(self, keys):
        self.check_jump_is_ok(keys)

        if self.current_state == 'stand':
            self.stand(keys)
        elif self.current_state == 'walk':
            self.walk(keys)
        elif self.current_state == 'jump':
            self.jump(keys)
        elif self.current_state == 'fall':
            self.fall(keys)
        elif self.current_state == 'die':
            self.die(keys)

        if self.face_right:
            self.mario_img = self.right_small_normal_imgs[self.mario_index]
        else:
            self.mario_img = self.left_small_normal_imgs[self.mario_index]

    def stand(self, keys):
        self.mario_index = 0
        self.x_speed = 0
        self.y_speed = 0

        if keys[pygame.K_RIGHT]:
            self.current_state = 'walk'
            self.face_right = True
        if keys[pygame.K_LEFT]:
            self.current_state = 'walk'
            self.face_right = False
        if keys[pygame.K_SPACE] and self.jump_ok:
            self.current_state = 'jump'
            self.y_speed = self.jump_velocity

    def walk(self, keys):
        if self.current_time - self.walking_time > self.calculate_frequency():
            self.walking_time = self.current_time

            if self.mario_index < 3:
                self.mario_index += 1
            else:
                self.mario_index = 1

        if keys[pygame.K_SPACE] and self.jump_ok:
            self.current_state = 'jump'
            self.y_speed = self.jump_velocity

        if keys[pygame.K_RIGHT]:
            self.face_right = True
            if self.x_speed < 0:
                self.mario_index = 5
            self.x_speed = self.calculate_speed(self.x_speed, self.walk_accel, self.max_walk_speed, is_right=True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_speed > 0:
                self.mario_index = 5
            self.x_speed = self.calculate_speed(self.x_speed, self.turn_accel, self.max_walk_speed, is_right=False)
        else:
            if self.face_right:
                self.x_speed -= self.walk_accel
                if self.x_speed <= 0:
                    self.x_speed = 0
                    self.current_state = 'stand'
            else:
                self.x_speed += self.walk_accel
                if self.x_speed >= 0:
                    self.x_speed = 0
                    self.current_state = 'stand'

    def jump(self, keys):
        self.mario_index = 4
        self.y_speed += self.anti_gravity
        self.jump_ok = False

        if self.y_speed >= 0:
            self.current_state = 'fall'

        if keys[pygame.K_RIGHT]:
            self.x_speed = self.calculate_speed(self.x_speed, self.x_accel, self.max_x_speed, is_right=True)
        elif keys[pygame.K_LEFT]:
            self.x_speed = self.calculate_speed(self.x_speed, self.x_accel, self.max_x_speed, is_right=False)

        if not keys[pygame.K_SPACE]:
            self.current_state = 'fall'

    def fall(self, keys):
        self.y_speed = self.calculate_speed(self.y_speed, self.gravity, self.max_y_velocity)

        if keys[pygame.K_RIGHT]:
            self.x_speed = self.calculate_speed(self.x_speed, self.walk_accel, self.max_walk_speed, is_right=True)
        elif keys[pygame.K_LEFT]:
            self.x_speed = self.calculate_speed(self.x_speed, self.walk_accel, self.max_walk_speed, is_right=False)

    def die(self, keys):
        self.rect.y += self.y_speed
        self.y_speed += self.anti_gravity

    def go_die(self):
        self.dead = True
        self.y_speed = self.jump_velocity
        self.mario_index = 6
        self.current_state = 'die'
        self.death_time = self.current_time

    def calculate_speed(self, cur_speed, a, max_speed, is_right=True):
        if is_right:
            return min(cur_speed + a, max_speed)
        return max(cur_speed - a, -max_speed)

    def calculate_frequency(self):
        frequency = -60 / self.max_run_speed * abs(self.x_speed) + 80

        return frequency

    def update(self, *args, **kwargs):
        self.current_time = pygame.time.get_ticks()
        keys = kwargs['keys']
        self.handel_states(keys)
        if keys[pygame.K_SPACE]:
            self.current_state = 'jump'
            self.y_speed = -5
        if self.current_state == 'walk':
            if self.current_time - self.walking_time > 100:
                self.walking_time = self.current_time
                self.mario_index += 1
                self.mario_index %= 4
        if self.current_state == 'jump':
            self.mario_index = 4
