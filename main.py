import pygame as pg
import constants as c
from obstacle import Obstacle
from player import Player
import random
import time

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
player = Player()

floor = pg.rect.Rect(0, c.SCREEN_HEIGHT * 0.7 , c.SCREEN_WIDTH, 10)
obstacles = pg.sprite.Group()
last_obstacle_spawned = pg.time.get_ticks()
obstacle_spawned = False
start_cooldown = 2500

game_over = False
game_over_time = None
large_font = pg.font.Font('freesansbold.ttf', 40)

def draw_text(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


running = True
while running:
    clock.tick(c.FPS)
    screen.fill((0, 0, 0))
    if not game_over:
        player.draw(screen)
        player.update(screen)
        pg.draw.rect(screen, (255, 255, 255), floor)

        if pg.time.get_ticks() - last_obstacle_spawned > start_cooldown:
            obstacles.add(Obstacle())
            last_obstacle_spawned = pg.time.get_ticks()

        obstacles.draw(screen)
        for obstacle in obstacles:
            obstacle.update(player)
            if obstacle.collided:
                game_over = True

    if game_over:
        if game_over_time == None:
            game_over_time = pg.time.get_ticks()
            obstacle_spawned = False
            for obstacle in obstacles:
                obstacle.kill()
        draw_text("GAME OVER", large_font, (255, 255, 255), c.SCREEN_WIDTH * 0.35, c.SCREEN_HEIGHT // 2 - 100)
        if pg.time.get_ticks() - game_over_time > 5000:
            game_over = False
            game_over_time = None


    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and player.jump_counter < 2:
                player.jump_counter += 1
                player.y_change = 18
            if event.key == pg.K_r:
                game_over = False
                game_over_time = None

    #if player.rect.y + 100 == c.SCREEN_HEIGHT * 0.7:
        #player.jump_counter = 0
    if player.rect.bottom >= c.SCREEN_HEIGHT * 0.7 and player.y_change <= 0:
        player.rect.bottom = c.SCREEN_HEIGHT * 0.7
        player.jump_counter = 0



    pg.display.flip()



pg.quit()