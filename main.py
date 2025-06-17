import pygame as pg
import constants as c
from obstacle import Obstacle
from player import Player
import random

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
player = Player()

floor = pg.rect.Rect(0, c.SCREEN_HEIGHT * 0.7 , c.SCREEN_WIDTH, 10)
obstacles = pg.sprite.Group()
for i in range(100):
    obstacles.add(Obstacle())

running = True
while running:
    clock.tick(c.FPS)
    screen.fill((0, 0, 0))
    player.draw(screen)
    player.update(screen)
    pg.draw.rect(screen, (255, 255, 255), floor)

    for obstacle in obstacles:
        obstacle.draw(screen)
        timer = pg.time.get_ticks()

    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and player.jump_counter < 2:
                player.jump_counter += 1
                player.y_change = 18

    #if player.rect.y + 100 == c.SCREEN_HEIGHT * 0.7:
        #player.jump_counter = 0
    if player.rect.bottom >= c.SCREEN_HEIGHT * 0.7 and player.y_change <= 0:
        player.rect.bottom = c.SCREEN_HEIGHT * 0.7
        player.jump_counter = 0


    pg.display.flip()
pg.quit()