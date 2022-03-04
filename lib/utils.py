import pygame
import os


def get_imgs(img_path):
    img_dict = {}
    for file in os.listdir(img_path):
        name, ext = os.path.splitext(file)
        img = pygame.image.load(os.path.join(img_path, file))
        # use convert method and faster blit
        if img.get_alpha():
            img = img.convert_alpha()
        else:
            img = img.convert()
        img_dict[name] = img

    return img_dict


def load_img(img, loc, size, colorkey, scale):
    # create a image surface
    img_surface = pygame.Surface(size)
    # add img to image surface
    img_surface.blit(img, (0, 0), (loc[0], loc[1], size[0], size[1]))
    # cutout img by color
    img_surface.set_colorkey(colorkey)
    # scale image surface
    img_surface = pygame.transform.scale(img_surface, (int(size[0] * scale), int(size[1] * scale)))

    return img_surface


