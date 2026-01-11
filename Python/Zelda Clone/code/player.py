import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.image = pygame.image.load('./graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.status = "down"
        self.speed = 5

    def movements(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y

    def inputs(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif key[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if key[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif key[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

    def update(self):
        self.inputs()
        self.movements()