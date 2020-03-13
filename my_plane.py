import pygame


class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("H:/images/me1.png")
        self.image2 = pygame.image.load("H:/images/me2.png")
        self.rect = self.image.get_rect()
        self.active = True
        self.destroy_image = []
        self.destroy_image.extend([
            pygame.image.load("H:/images/me_destroy_1.png").convert_alpha(),
            pygame.image.load("H:/images/me_destroy_2.png").convert_alpha(),
            pygame.image.load("H:/images/me_destroy_3.png").convert_alpha(),
            pygame.image.load("H:/images/me_destroy_4.png").convert_alpha()])
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2, \
            self.height - self.rect.height - 60
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image)
        self.Invincible = False

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDn(self):
        if self.rect.bottom < self.height:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height

    def moveLf(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRt(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2, \
            self.height - self.rect.height - 60
        self.active = True
        self.Invincible = True



