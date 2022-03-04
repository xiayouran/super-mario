import pygame
from lib.utils import get_imgs
from lib.constants import *


pygame.init()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('SuperMario')

IMAGEDICT = get_imgs(IMAGEPATH)

