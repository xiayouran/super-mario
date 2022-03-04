import sys
import pygame
from lib.init import IMAGEDICT, SCREEN
from lib.constants import *
from lib.utils import load_img
from lib.components.info import Info


class Main(object):
    def __init__(self, state_dict, start_state='main_menu'):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.keys = pygame.key.get_pressed()

        self.state_dict = state_dict
        self.state_obj = self.state_dict[start_state]

    def update(self):
        if self.state_obj.finish_flag:
            next_state = self.state_obj.next_state
            self.state_obj.finish_flag = False
            self.state_obj = self.state_dict[next_state]

        self.state_obj.update(self.screen, self.keys)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                if event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()

            self.update()

            # pygame.display.flip()
            pygame.display.update()
            # set FPS
            self.clock.tick(60)


class MainMenu(object):
    def __init__(self):
        self.setup_background()
        self.setup_player()
        self.setup_cursor()

        self.info = Info(state_str='main_menu')

        self.finish_flag = False
        self.next_state = 'load_screen'
        self.cursor_state = '1P'

    def setup_background(self):
        self.background = IMAGEDICT['level_1']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * SCALE),
                                                                   int(rect.height * SCALE)))
        self.window = SCREEN.get_rect()
        self.caption = load_img(IMAGEDICT['title_screen'], (1, 60), (176, 88), (255, 0, 220), SCALE)

    def setup_player(self):
        self.player = load_img(IMAGEDICT['mario_bros'], (178, 32), (12, 16), (0, 0, 0), SCALE)

    def setup_cursor(self):
        self.cursor = pygame.sprite.Sprite()
        self.cursor.image = load_img(IMAGEDICT['item_objects'], (24, 160), (8, 8), (0, 0, 0), SCALE)
        rect = self.cursor.image.get_rect()
        rect.x, rect.y = (220, 360)
        self.cursor.rect = rect

    def update_cursor(self, keys):
        if keys[pygame.K_UP]:
            self.cursor_state = '1P'
            self.cursor.rect.y = 360
        elif keys[pygame.K_DOWN]:
            self.cursor_state = '2P'
            self.cursor.rect.y = 405
        elif keys[pygame.K_RETURN]:
            if self.cursor_state == '1P':
                self.finish_flag = True
            elif self.cursor_state == '2P':
                self.finish_flag = True

    def update(self, surface, keys):
        self.update_cursor(keys)

        surface.blit(self.background, self.window)
        surface.blit(self.caption, (165, 100))
        surface.blit(self.player, (110, 494))
        surface.blit(self.cursor.image, self.cursor.rect)

        self.info.update()
        self.info.draw(surface)
