import pygame as pg
import constants as c
from TimePeriod import TimePeriod
from obstacle import Obstacle
from player import Player
import random
import json
import time

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
player = Player()
pg.mixer.init()
pg.mixer.music.set_volume(0.2)


floor = pg.rect.Rect(0, c.SCREEN_HEIGHT * 0.9 , c.SCREEN_WIDTH, 10)
obstacles = pg.sprite.Group()
last_obstacle_spawned = pg.time.get_ticks()
obstacle_spawned = False
start_cooldown = 2500
min_cooldown = 1
max_cooldown = 100

game_over = False
game_over_time = None
score = 0
hscore = 0
last_score_time = pg.time.get_ticks()
large_font = pg.font.Font('freesansbold.ttf', 30)
#chatgpt
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
#end of gpt
offset_float = random.uniform(0.7, 1.3)

#chatgpt
with open("assets_data.json", "r") as f:
    assets_data = json.load(f)

periods = []
for period_data in assets_data:
    period = TimePeriod(
        name=period_data["timeperiod"],
        background=period_data["background"],
        songs=period_data["songs"],
        obstacles=period_data["obstacles"],
        character=period_data["character"]
    )
    period.load_assets()
    periods.append(period)

current_period = periods[0]
current_period.load_assets()
current_period.start_next_song()
player.set_image(current_period.get_character())

def spawn_obstacle(current_period, speed, obstacles_group):
    if current_period.obstacles:
        # Choose a random obstacle surface from current period
        obstacle_img = random.choice(current_period.obstacles)
    else:
        obstacle_img = None  # fallback to placeholder

    new_obstacle = Obstacle(speed=speed, image=obstacle_img)
    obstacles_group.add(new_obstacle)

#end of gpt
def check_for_highscore(score, hscore):
    if score <= hscore:
        return hscore
    if score >= hscore:
        return score


running = True
while running:
    clock.tick(c.FPS)
    screen.fill((0, 0, 0))
    if not game_over:
        #chatgpt

        current_period.update()

        if not current_period.is_playing_song:
            # Start next song automatically or advance period if done
            if not current_period.start_next_song():
                # All songs done, advance to next period if score allows
                next_index = periods.index(current_period) + 1
                if next_index < len(periods) :
                    current_period = periods[next_index]
                    current_period.load_assets()
                    current_period.start_next_song()
                    player.set_image(current_period.get_character())
                    player.jump_counter = 0

        # draw background, character, song info etc
        current_period.draw_background(screen)
        current_period.draw_song_info(screen, large_font)
        #end of gpt


        player.draw(screen)
        player.update(screen)
        #pg.draw.rect(screen, (255, 255, 255), floor)

        score_cooldown = decay_cooldown(score)
        current_time = pg.time.get_ticks()
        if current_time - last_score_time > score_cooldown:
            score += 1
            last_score_time = current_time
            hscore = check_for_highscore(score, hscore)

        draw_text(f" HS: {hscore}", large_font, (255,255,255), 600, 0)
        draw_text(f"Score: {score}", large_font, (255,255,255), 20,0)
        '''
        the new code is fully gpt
        this was mine
        obstacle_speed = scale_speed(score)
        obstacle_spawn_cooldown = get_spawn_cooldown(obstacle_speed)

        if pg.time.get_ticks() - last_obstacle_spawned > obstacle_spawn_cooldown * offset_float:
            obstacles.add(Obstacle(speed=obstacle_speed))
            last_obstacle_spawned = pg.time.get_ticks()
            if random.randint(1,3) == 2:
                obstacles.add(Obstacle(speed=obstacle_speed, offset_x=int(50* offset_float)))
            if random.randint(1,3) == 3:
                obstacles.add(Obstacle(speed=obstacle_speed ,offset_x=int(50* offset_float)))
            offset_float = random.uniform(0.7, 1.3)
        '''

        # Calculate obstacle speed and cooldown dynamically
        obstacle_speed = scale_speed(score)
        obstacle_spawn_cooldown = get_spawn_cooldown(obstacle_speed)

        # Time to spawn a new obstacle
        if pg.time.get_ticks() - last_obstacle_spawned > obstacle_spawn_cooldown * offset_float:
            # Get a random obstacle image from the current period
            obstacle_image = current_period.get_next_obstacle()

            # Always spawn at least one obstacle
            obstacles.add(Obstacle(image=obstacle_image, speed=obstacle_speed))

            # Random chance for a second or third obstacle with x-offset
            if random.randint(1, 3) == 2:
                obstacles.add(Obstacle(image=obstacle_image, speed=obstacle_speed, offset_x=int(90)))
            if random.randint(1, 5) == 3:
                obstacles.add(Obstacle(image=obstacle_image, speed=obstacle_speed, offset_x=int(180)))

            # Update time and offset for next spawn
            last_obstacle_spawned = pg.time.get_ticks()
            offset_float = random.uniform(0.7, 1.3)


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
        if pg.time.get_ticks() - game_over_time > 2000:
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
    if player.rect.bottom >= c.SCREEN_HEIGHT * 0.9 -20 and player.y_change <= 0:
        player.rect.bottom = c.SCREEN_HEIGHT * 0.9
        player.jump_counter = 0



    pg.display.flip()



pg.quit()