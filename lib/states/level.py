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

    def setup_background(self):
        self.background = IMAGEDICT['level_1']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * SCALE),
                                                                   int(rect.height * SCALE)))

    def setup_plater(self):
        self.player = Player(name='mario')
        self.player.rect.x = 300
        self.player.rect.y = 300

    def update_position(self):
        pass

    def update(self, surface, keys):
        self.draw(surface)

        self.player.update(keys=keys)
        self.update_position()

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self.info.draw(surface)
        self.info.update()

