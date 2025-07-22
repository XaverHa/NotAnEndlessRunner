import pygame as pg
import os
import random

class TimePeriod:
    def __init__(self, name, background, songs, obstacles, character):
        self.name = name
        self.background_path = background
        self.songs = songs                      # list of dicts with song info (including 'duration' in seconds)
        self.obstacles = obstacles
        self.character_path = character

        self.background = None
        self.character = None

        self.current_song_index = 0
        self.current_song_start_time = 0
        self.current_song = None
        self.is_playing_song = False

    def load_assets(self):
        self.background = pg.image.load(self.background_path).convert()
        self.character = pg.image.load(self.character_path).convert_alpha()
        self.obstacle_images = []

        for path in self.obstacles:
            self.obstacle_images.append(pg.image.load(path).convert_alpha())

    def draw_background(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))

    def get_character(self):
        return self.character

    def start_next_song(self):
        if self.current_song_index >= len(self.songs):
            self.is_playing_song = False
            self.current_song = None
            return False  # no more songs to play in this period

        song_data = self.songs[self.current_song_index]
        pg.mixer.music.load(song_data["file"])
        pg.mixer.music.play()
        self.current_song = song_data
        self.current_song_start_time = pg.time.get_ticks()
        self.is_playing_song = True
        self.current_song_index += 1
        return True

    def update(self):
        # Call this every frame to check if current song snippet finished
        if self.is_playing_song and self.current_song:
            elapsed_sec = (pg.time.get_ticks() - self.current_song_start_time) / 1000
            if elapsed_sec >= self.current_song.get("duration", 30):
                pg.mixer.music.stop()
                self.is_playing_song = False
                self.current_song = None

    def draw_song_info(self, screen, font):
        if self.current_song:
            band = f"{self.current_song['artist']} - {self.current_song['title']}"
            year = f"{self.current_song['year']} - {self.current_song['album']}"
            upper = font.render(band, True, (255, 255, 255))
            lower = font.render(year, True, (255, 255, 255))
            screen.blit(upper, (20, 30))
            screen.blit(lower, (20, 60))

    def get_next_obstacle(self):
        if not self.obstacle_images:
            return None
        return random.choice(self.obstacle_images)

    def is_done(self):
        # True if all songs played and no song currently playing
        return (self.current_song_index >= len(self.songs)) and (not self.is_playing_song)
