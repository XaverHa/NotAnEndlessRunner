import constants as c
import pygame as pg

class Player:
    def __init__(self):
        self.pos = (c.SCREEN_WIDTH * 0.1, c.SCREEN_HEIGHT * 0.9 - 100)
        self.image = pg.Surface((100, 100))  # placeholder    # white box for now
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=self.pos)
        self.y_change = 0
        self.jump_counter = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    #chatgpt suggestion
    def set_image(self, new_image):
        self.image = new_image
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
    #end of gpt

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
