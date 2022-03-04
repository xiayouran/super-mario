import pygame
from lib.constants import *
from lib.components.coin import TwinklingCoin
from lib.utils import load_img
from lib.init import IMAGEDICT


class Info(object):
    def __init__(self, state_str):
        self.state_str = state_str

        self.create_state_text()
        self.create_info_text()

        self.twinkling_coin = TwinklingCoin()

    def create_state_text(self):
        if self.state_str == 'main_menu':
            self.create_main_menu_text()
        elif self.state_str == 'load_screen':
            self.create_load_screen_text()
        elif self.state_str == 'level':
            self.create_level_text()

    def create_info_text(self):
        self.info_text = []

        self.info_text.append((self.create_text('MARIO'), (75, 30)))
        self.info_text.append((self.create_text('WORLD'), (450, 30)))
        self.info_text.append((self.create_text('TIME'), (625, 30)))
        self.info_text.append((self.create_text('000000'), (75, 55)))
        self.info_text.append((self.create_text('×00'), (300, 55)))
        self.info_text.append((self.create_text('1-1'), (470, 55)))

    def create_text(self, text, size=45, wscale=1.25, hscale=1.0):
        font = pygame.font.Font(FONTPATH, size)
        text_img = font.render(text, False, (255, 255, 255))
        # text_rect = text_img.get_rect()
        # text_img = pygame.transform.scale(text_img, (int(text_rect.width * wscale), int(text_rect.height * hscale)))

        return text_img

    def create_main_menu_text(self):
        self.state_text = []

        self.state_text.append((self.create_text('1   PLAYER  GAME'), (272, 350)))
        self.state_text.append((self.create_text('2   PLAYER  GAME'), (272, 395)))
        self.state_text.append((self.create_text('TOP - '), (300, 450)))
        self.state_text.append((self.create_text('000000'), (410, 450)))

    def create_load_screen_text(self):
        self.state_text = []

        self.state_text.append((self.create_text('WORLD'), (280, 200)))
        self.state_text.append((self.create_text('1 - 1'), (430, 200)))
        self.state_text.append((self.create_text('× 3'), (380, 280)))

        self.player_img = load_img(IMAGEDICT['mario_bros'], (178, 32), (12, 16), (0, 0, 0), SCALE)

    def create_level_text(self):
        self.state_text = []

    def update(self):
        self.twinkling_coin.update()

    def draw(self, surface):
        for text in self.state_text:
            surface.blit(text[0], text[1])

        for text in self.info_text:
            surface.blit(text[0], text[1])

        surface.blit(self.twinkling_coin.coin_img, self.twinkling_coin.menu_loc)

        if self.state_str == 'load_screen':
            surface.blit(self.player_img, (300, 270))
