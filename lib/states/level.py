import pygame
from lib.components.info import Info
from lib.init import IMAGEDICT
from lib.constants import *
from lib.components.player import Player


class Level(object):
    def __init__(self):
        self.finish_flag = False
        self.next_state = None

        self.info = Info(state_str='level')
        self.setup_background()
        self.setup_player()

    def setup_background(self):
        self.background = IMAGEDICT['level_1']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * SCALE),
                                                                   int(rect.height * SCALE)))

    def setup_player(self):
        self.player = Player(name='mario')
        self.player.rect.x = 300
        self.player.rect.y = 300

    def update_position(self):
        self.player.rect.x += self.player.x_speed
        self.player.rect.y += self.player.y_speed

    def update(self, surface, keys):
        self.draw(surface)

        self.player.update(keys=keys)
        self.update_position()

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.player.mario_img, self.player.rect)
        self.info.draw(surface)
        self.info.update()

