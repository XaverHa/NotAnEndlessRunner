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
min_cooldown = 1
max_cooldown = 100

game_over = False
game_over_time = None
score = 0
last_score_time = pg.time.get_ticks()

large_font = pg.font.Font('freesansbold.ttf', 40)
def draw_text(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
def decay_cooldown(score, base=40, minimum=1, decay_rate=0.97, scale=100):
    factor = decay_rate ** (score / scale)
    return max(minimum, int(base * factor))
def scale_speed(score, base_speed=7.5, max_speed=25.0, growth_rate=1.015, scale=100):
    raw_speed = base_speed * (growth_rate ** (score / scale))
    return min(max_speed, raw_speed)
def get_spawn_cooldown(speed, min_spacing_px=start_cooldown):
    frames_needed = min_spacing_px / speed  # How many frames to cover spacing
    return int(frames_needed * (1000 / 60))  # Convert to ms (assuming 60 FPS)




running = True
while running:
    clock.tick(c.FPS)
    screen.fill((0, 0, 0))
    if not game_over:
        player.draw(screen)
        player.update(screen)
        pg.draw.rect(screen, (255, 255, 255), floor)

        score_cooldown = decay_cooldown(score)
        current_time = pg.time.get_ticks()
        if current_time - last_score_time > score_cooldown:
            score += 1
            last_score_time = current_time

        draw_text(f"Score: {score}", large_font, (255,255,255), 0,0)

        obstacle_speed = scale_speed(score)
        obstacle_spawn_cooldown = get_spawn_cooldown(obstacle_speed)

        if pg.time.get_ticks() - last_obstacle_spawned > obstacle_spawn_cooldown:
            obstacles.add(Obstacle(speed=obstacle_speed))
            last_obstacle_spawned = pg.time.get_ticks()

        obstacles.draw(screen)
        for obstacle in obstacles:
            obstacle.update(player)
            if obstacle.collided:
                game_over = True

    if game_over:
        if game_over_time == None:
            score = 0
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