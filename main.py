import pgzrun
from random import randint
from pygame import Rect
import sys

WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 7
ENEMY_SPEED = 1

background_music = "sounds/background_music.wav"
collect_sound = "sounds/collect.wav"
game_over_sound = "sounds/game_over.wav"
checkpoint_sound = "sounds/checkpoint.wav"

background = Actor("sand")

player_images = {
    'stand': 'player/player_stand',
    'walk_right': ['player/p1_walk01', 'player/p1_walk02', 'player/p1_walk03', 'player/p1_walk04', 'player/p1_walk05', 'player/p1_walk06', 'player/p1_walk07'],
    'walk_left': ['player/p1_walk01', 'player/p1_walk02', 'player/p1_walk03', 'player/p1_walk04', 'player/p1_walk05', 'player/p1_walk06', 'player/p1_walk07'],
    'walk_up': ['player/p1_walk01', 'player/p1_walk02', 'player/p1_walk03', 'player/p1_walk04', 'player/p1_walk05', 'player/p1_walk06', 'player/p1_walk07'],
    'walk_down': ['player/p1_walk01', 'player/p1_walk02', 'player/p1_walk03', 'player/p1_walk04', 'player/p1_walk05', 'player/p1_walk06', 'player/p1_walk07']
}
player = Actor(player_images['stand'], (400, 500))
player_frame = 0

enemies = [Actor("ghost")]
enemy_directions = [(1, 1)]
diamond = Actor("diamond", pos=(300, 300))
score = 0
level = 1
game_over = False
game_over_image = Actor("game_over", center=(WIDTH // 2, HEIGHT // 2))
music_muted = False

sounds.background_music.play(-1)

game_started = False
play_button = Actor("play_button", center=(WIDTH // 2, HEIGHT // 2))
exit_button = Actor("exit_button", center=(WIDTH // 2, HEIGHT // 2 + 100))
mute_button = Actor("mute_button", topright=(WIDTH - 10, 10))
unmute_button = Actor("unmute_button", topright=(WIDTH - 10, 10))

def draw():
    screen.clear()
    background.draw()
    if not game_started:
        draw_start_screen()
    elif game_over:
        game_over_image.draw()
    else:
        player.draw()
        for enemy in enemies:
            enemy.draw()
        diamond.draw()
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="black")
        screen.draw.text(f"Level: {level}", (10, 50), fontsize=40, color="blue")
        if music_muted:
            mute_button.draw()
        else:
            unmute_button.draw()

def draw_start_screen():
    screen.draw.text("Ghost Escape", center=(WIDTH // 2, HEIGHT // 2 - 150), fontsize=60, color="white")
    play_button.draw()
    exit_button.draw()
    if music_muted:
        mute_button.draw()
    else:
        unmute_button.draw()

def update():
    global score, level, game_over

    if game_over or not game_started:
        return

    move_player()
    move_enemies()

    if diamond.colliderect(player):
        diamond.x = randint(0, WIDTH - diamond.width)
        diamond.y = randint(0, HEIGHT - diamond.height)
        score += 1
        sounds.collect.play()
        if score % 5 == 0:
            add_enemy()
            level += 1
            sounds.checkpoint.play()


def move_player():
    global player_frame

    if keyboard.right:
        player.x += PLAYER_SPEED
        player_frame = (player_frame + 1) % len(player_images['walk_right'])
        player.image = player_images['walk_right'][player_frame]
    elif keyboard.left:
        player.x -= PLAYER_SPEED
        player_frame = (player_frame + 1) % len(player_images['walk_left'])
        player.image = player_images['walk_left'][player_frame]
    elif keyboard.up:
        player.y -= PLAYER_SPEED
        player_frame = (player_frame + 1) % len(player_images['walk_up'])
        player.image = player_images['walk_up'][player_frame]
    elif keyboard.down:
        player.y += PLAYER_SPEED
        player_frame = (player_frame + 1) % len(player_images['walk_down'])
        player.image = player_images['walk_down'][player_frame]
    else:
        player.image = player_images['stand']  # Stand still image

    wrap_around_screen(player)

def move_enemies():
    global game_over
    for i, enemy in enumerate(enemies):
        direction = enemy_directions[i]
        if enemy.x < player.x:
            enemy.x += ENEMY_SPEED * direction[0]
        if enemy.x > player.x:
            enemy.x -= ENEMY_SPEED * direction[0]
        if enemy.y < player.y:
            enemy.y += ENEMY_SPEED * direction[1]
        if enemy.y > player.y:
            enemy.y -= ENEMY_SPEED * direction[1]
        if player.colliderect(enemy):
            game_over = True
            sounds.background_music.stop()
            sounds.game_over.play()

def add_enemy():
    x = randint(0, WIDTH - 50)
    y = randint(0, HEIGHT - 50)
    direction = (randint(0, 1) * 2 - 1, randint(0, 1) * 2 - 1) 
    new_enemy = Actor("ghost", (x, y))
    enemies.append(new_enemy)
    enemy_directions.append(direction)

def wrap_around_screen(actor):
    if actor.x > WIDTH:
        actor.x = 0
    if actor.x < 0:
        actor.x = WIDTH
    if actor.y < 0:
        actor.y = HEIGHT
    if actor.y > HEIGHT:
        actor.y = 0

def on_mouse_down(pos):
    global game_started, music_muted
    if play_button.collidepoint(pos):
        game_started = True
    elif exit_button.collidepoint(pos):
        sys.exit()
    elif mute_button.collidepoint(pos) and not music_muted:
        sounds.background_music.stop()
        music_muted = True
    elif unmute_button.collidepoint(pos) and music_muted:
        sounds.background_music.play(-1)
        music_muted = False

def on_key_down(key):
    global music_muted
    if key == keys.M:
        if music_muted:
            sounds.background_music.play(-1)
        else:
            sounds.background_music.stop()
        music_muted = not music_muted

pgzrun.go()