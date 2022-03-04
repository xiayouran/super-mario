import sys
import pygame
from lib.init import IMAGEDICT, SCREEN
from lib.constants import *
from lib.utils import load_img
from lib.components.info import Info


class Main(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

    def run(self, menu):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                if event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()

            menu.update(self.screen)

            # pygame.display.flip()
            pygame.display.update()
            # set FPS
            self.clock.tick(60)


class MainMenu(object):
    def __init__(self):
        self.setup_background()
        self.setup_player()
        self.setup_cursor()

        self.info = Info('main_menu')

    def setup_background(self):
        self.background = IMAGEDICT['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * SCALE),
                                                                   int(self.background_rect.height * SCALE)))
        self.window = SCREEN.get_rect()
        self.caption = load_img(IMAGEDICT['title_screen'], (1, 60), (176, 88), (255, 0, 220), SCALE)

    def setup_player(self):
        self.player = load_img(IMAGEDICT['mario_bros'], (178, 32), (12, 16), (0, 0, 0), SCALE)

    def setup_cursor(self):
        self.cursor = load_img(IMAGEDICT['item_objects'], (24, 160), (8, 8), (0, 0, 0), SCALE)

    def update(self, surface):
        surface.blit(self.background, self.window)
        surface.blit(self.caption, (165, 100))
        surface.blit(self.player, (110, 494))
        surface.blit(self.cursor, (220, 360))

        self.info.update()
        self.info.draw(surface)
