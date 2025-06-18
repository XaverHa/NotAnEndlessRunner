SCREEN_WIDTH = 768
SCREEN_HEIGHT = 512
FPS = 60
GRAVITY = 1

ASSETS = [
    {
        "timeperiod": "early60s",
        "background": "assets/images/backgrounds/early60s_bg.png",
        "character": "assets/images/player/early60s_char2.png",
        "songs": [
            {
                "file": "assets/music/beatles_twist_and_shout.mp3",
                "artist": "The Beatles",
                "album": "Please Please Me",
                "year": 1963,
                "title": "Twist and Shout",
                "duration": 30  # seconds to play
            },
            {
                "file": "assets/music/beatles_love_me_do.mp3",
                "artist": "The Beatles",
                "album": "Please Please Me",
                "year": 1963,
                "title": "Love Me Do",
                "duration": 30
            }
        ],
        "obstacles": [
            "assets/images/obstacles/old_radio.png",
            "assets/images/obstacles/vintage_car.png"
        ]
    },
    {
        "timeperiod": "late60s",
        "background": "assets/images/backgrounds/late60s_bg.png",
        "character": "assets/images/player/late60s_char.png",
        "songs": [
            {
                "file": "assets/music/stones_satisfaction.mp3",
                "artist": "The Rolling Stones",
                "album": "Out of Our Heads",
                "year": 1965,
                "title": "(I Can't Get No) Satisfaction",
                "duration": 40
            }
        ],
        "obstacles": [
            "assets/images/obstacles/flower_power.png"
        ]
    }
]