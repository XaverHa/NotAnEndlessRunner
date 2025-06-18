import pygame as pg
import random
import constants as c

class Obstacle(pg.sprite.Sprite):
    def __init__(self, image=None, speed=7.5, offset_x=0):
        super().__init__()
        self.speed = speed

        if image:
            self.image = image
        else:
            size_category = random.choice(['small', 'medium', 'large'])
            size = {'small': (30, 30), 'medium': (50, 50), 'large': (80, 80)}[size_category]
            color = random.choice([(200, 50, 50), (50, 200, 50), (50, 50, 200)])
            self.image = pg.Surface(size)
            self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.left = c.SCREEN_WIDTH + 20 + offset_x
        self.rect.bottom = c.SCREEN_HEIGHT * 0.9
        self.collided = False

    def update(self, player):
        self.rect.x -= self.speed
        self.check_collision(player)
        self.destroy_if_offscreen()

    def check_collision(self,player):
        if player.rect.colliderect(self.rect):
            self.collided = True
    def destroy_if_offscreen(self):
        if self.rect.x < -100:
            self.kill()
