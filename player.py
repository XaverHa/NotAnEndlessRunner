import constants as c
import pygame as pg

class Player:
    def __init__(self):
        self.pos = (c.SCREEN_WIDTH * 0.2, c.SCREEN_HEIGHT * 0.7 - 100)
        self.image = pg.Surface((100, 100))  # placeholder
        self.image.fill((255, 255, 255))     # white box for now
        self.rect = self.image.get_rect(topleft=self.pos)
        self.y_change = 0
        self.jump_counter = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, screen):
        self.jump()

    def jump(self):
        if self.rect.y > 0 or self.rect.y < self.pos[1]:
            self.rect.y -= self.y_change
            self.y_change -= c.GRAVITY
        if self.rect.y > self.pos[1]:
            self.rect.y = self.pos[1]
        if self.rect.y == self.pos[1] and self.y_change < 0:
            self.y_change = 0
