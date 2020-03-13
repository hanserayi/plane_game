import pygame
from random import *


class Small_enemy(pygame.sprite.Sprite):
    energy = 1

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("H:/images/enemy1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.active = True
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("H:/images/enemy1_down1.png").convert_alpha(),
            pygame.image.load("H:/images/enemy1_down2.png").convert_alpha(),
            pygame.image.load("H:/images/enemy1_down3.png").convert_alpha(),
            pygame.image.load("H:/images/enemy1_down4.png").convert_alpha()])
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-5 * self.height, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-5 * self.height, 0)
        self.active = True


class Mid_enemy(pygame.sprite.Sprite):
    energy = 8

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("H:/images/enemy2.png").convert_alpha()
        self.image_hit = pygame.image.load("H:/images/enemy2_hit.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.active = True
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("H:/images/enemy2_down1.png").convert_alpha(),
            pygame.image.load("H:/images/enemy2_down2.png").convert_alpha(),
            pygame.image.load("H:/images/enemy2_down3.png").convert_alpha(),
            pygame.image.load("H:/images/enemy2_down4.png").convert_alpha()])
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, -2 * self.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = Mid_enemy.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, -2 * self.height)
        self.active = True
        self.energy = Mid_enemy.energy
        self.hit = False


class Big_enemy(pygame.sprite.Sprite):
    energy = 20

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("H:/images/enemy3_n1.png").convert_alpha()
        self.image_2 = pygame.image.load("H:/images/enemy3_n2.png").convert_alpha()
        self.image_hit = pygame.image.load("H:/images/enemy3_hit.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.active = True
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("H:/images/enemy3_down1.png").convert_alpha(),
            pygame.image.load("H:/images/enemy3_down2.png").convert_alpha(),
            pygame.image.load("H:/images/enemy3_down3.png").convert_alpha(),
            pygame.image.load("H:/images/enemy3_down4.png").convert_alpha(),
            pygame.image.load("H:/images/enemy3_down5.png").convert_alpha(),
            pygame.image.load("H:/images/enemy3_down6.png").convert_alpha()])
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-20 * self.height, -5 * self.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = Big_enemy.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-20 * self.height, -5 * self.height)
        self.active = True
        self.energy = Big_enemy.energy
        self.hit = False
