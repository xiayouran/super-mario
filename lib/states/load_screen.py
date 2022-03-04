import pygame.time
from lib.components.info import Info


class LoadScreen(object):
    def __init__(self):
        self.finish_flag = False
        self.next_state = 'level'
        self.timer = 0

        self.info = Info(state_str='load_screen')

    def update(self, surface, keys):
        self.draw(surface)

        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif (pygame.time.get_ticks() - self.timer) > 3000:
            self.finish_flag = True
            self.timer = 0

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.info.draw(surface)
        self.info.update()
