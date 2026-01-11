import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type, surface=pygame.surface.Surface((64, 64))):
        super().__init__(groups)
        self.sprite_type = type
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        