import pygame


class RoundSprite(pygame.sprite.Sprite):
    def __init__(self, color, radius, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((radius*2, radius*2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.radius = radius

    def update(self):
        pass