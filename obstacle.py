import pygame as pg
import random
import constants as c

class Obstacle(pg.sprite.Sprite):
    def __init__(self, speed=7.5):
        super().__init__()  # Required for Sprite subclassing
        self.speed = speed

        size_category = random.choice(['small', 'medium', 'large'])
        if size_category == 'small':
            self.size = (30, 30)
        elif size_category == 'medium':
            self.size = (50, 50)
        else:
            self.size = (80, 80)

        self.color = random.choice([
            (200, 50, 50),
            (50, 200, 50),
            (50, 50, 200),
        ])

        self.image = pg.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.left = c.SCREEN_WIDTH + random.randint(0, 100)
        self.rect.bottom = c.SCREEN_HEIGHT * 0.7

        self.collided = False

    def update(self, player):
        self.rect.x -= self.speed
        self.check_collision(player)

    def check_collision(self,player):
        if player.rect.colliderect(self.rect):
            self.collided = True