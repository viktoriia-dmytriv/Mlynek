import pygame

import consts
from simple_sprite import SimpleSprite


class ButtonSprite(SimpleSprite):
    def __init__(self, player, is_player, position, radius):
        sprite_sheet = pygame.image.load("resources\\buttons.png")
        image = sprite_sheet.subsurface(consts.BUTTON_SPRITE_POS[player][is_player] + (32, 32))
        image = pygame.transform.scale(image, (radius * 2, radius * 2))
        SimpleSprite.__init__(self, image, position)
        self.radius = radius
        self.is_player = is_player
        self.player = player
