import pygame

import consts
from round_sprite import RoundSprite
from simple_sprite import SimpleSprite


class ChipSprite(SimpleSprite):
    def __init__(self, player, position, radius):
        sprite_sheet = pygame.image.load("resources\chips.png")
        # take sprite from sprite sheet (third picture in the row)
        image = sprite_sheet.subsurface(consts.CHIP_SPRITE_POS[player] + (32, 32))
        image = pygame.transform.scale(image, (radius * 2, radius * 2))
        SimpleSprite.__init__(self, image, position)
        self.radius = radius
