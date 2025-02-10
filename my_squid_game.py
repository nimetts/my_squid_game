import pgzrun
import random
from pygame import Rect

WIDTH, HEIGHT = 1000, 700
background = Actor("background", (WIDTH // 2, HEIGHT // 2))
TITLE = "Squid Game"
game_state = "menu"
time_left = 20
music.play("background_music")
music.set_volume(0.5)
enemy_count = 10

class Button(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.original_pos = pos

    def is_clicked(self, pos):
        return self.colliderect(Rect(pos, (1, 1)))

    def move_to_center(self):
        self.x = self.original_pos[0]
        self.y = self.original_pos[1]


start_button = Button("start_button", (WIDTH // 2, HEIGHT // 2 - 50))
start_button.move_to_center()
quit_button = Button("quit_button", (WIDTH // 2, HEIGHT // 2 + 50))
quit_button.move_to_center()
restart_button = Button("restart_button", (WIDTH // 2, HEIGHT // 2 - 50))
restart_button.move_to_center()
music_button = Button("music_on", (WIDTH // 2, HEIGHT // 2 + 150))
music_playing = True

hero_1_button = Button("hero_1_button", (WIDTH // 2 - 150, HEIGHT // 2))
hero_2_button = Button("hero_2_button", (WIDTH // 2 + 150, HEIGHT // 2))

class Hero:
    def __init__(self, character="hero_1"):
        self.character = character
        if self.character == "hero_1":
            self.images = ["hero_1", "hero_idle_1"]
        else:
            self.images = ["hero_2", "hero_idle_2"]
        self.index = 0
        self.sprite = Actor(self.images[self.index], (WIDTH // 2, HEIGHT // 2))
        self.speed = 5
        self.timer = 0
        self.idle_timer = 0
        self.moving = False
        self.health = 100

    def move(self):
        self.moving = False
        if keyboard.left and self.sprite.left > 0:
            self.sprite.x -= self.speed
            self.moving = True
        if keyboard.right and self.sprite.right < WIDTH:
            self.sprite.x += self.speed
            self.moving = True
        if keyboard.up and self.sprite.top > 0:
            self.sprite.y -= self.speed
            self.moving = True
        if keyboard.down and self.sprite.bottom < HEIGHT:
            self.sprite.y += self.speed
            self.moving = True
        if self.moving:
            self.idle_timer = 0
        else:
            self.idle_timer += 1

    def animate(self):
        self.timer += 1
        if self.moving:
            if self.timer % 10 == 0:
                self.index = (self.index + 1) % 2
                self.sprite.image = self.images[self.index]
        else:
            if self.timer % 30 == 0:
                self.index = 0 if self.index < 1 else 1
                self.sprite.image = self.images[self.index]
            if self.timer % 50 == 0:
                self.sprite.y += 1
            elif self.timer % 50 == 25:
                self.sprite.y -= 1

    def draw(self):
        self.sprite.draw()
        screen.draw.rect(Rect((10, 10), (self.health * 2, 20)), color="red")
        screen.draw.text("Health", (self.health * 2 + 15, 10), fontsize=20, color="red")


class Enemy:
    def __init__(self, x, y, type):
        if type == "enemy_1":
            self.images = ["enemy_1", "enemy_idle_1"]
        else:
            self.images = ["enemy_2", "enemy_idle_2"]
        self.index = 0
        self.sprite = Actor(self.images[self.index], (x, y))
        self.direction = random.choice(["horizontal", "vertical", "diagonal", "random"])
        self.speed = random.randint(3, 6)
        self.timer = 0
        self.health = 50
        self.direction_timer = 0
        self.type = type
        self.damage = 20 if self.type == "enemy_1" else 10

    def move(self):
        self.direction_timer += 1

        if self.direction_timer >= random.randint(180, 240):
            self.direction = random.choice(["horizontal", "vertical", "diagonal", "random"])
            self.direction_timer = 0

            if self.speed == 0:
                self.speed = random.choice([-6, -5, -4, 3, 4, 5, 6])

        if self.direction == "horizontal":
            self.sprite.x += self.speed
            if self.sprite.right > WIDTH or self.sprite.left < 0:
                self.speed *= -1
        elif self.direction == "vertical":
            self.sprite.y += self.speed
            if self.sprite.bottom > HEIGHT or self.sprite.top < 0:
                self.speed *= -1
        elif self.direction == "diagonal":
            self.sprite.x += self.speed
            self.sprite.y += self.speed
            if self.sprite.right > WIDTH or self.sprite.left < 0 or self.sprite.bottom > HEIGHT or self.sprite.top < 0:
                self.speed *= -1
        elif self.direction == "random":
            move_direction = random.choice(["up", "down", "left", "right"])
            if move_direction == "up":
                self.sprite.y -= abs(self.speed)
            elif move_direction == "down":
                self.sprite.y += abs(self.speed)
            elif move_direction == "left":
                self.sprite.x -= abs(self.speed)
            elif move_direction == "right":
                self.sprite.x += abs(self.speed)

            if self.sprite.left < 0 or self.sprite.right > WIDTH or self.sprite.top < 0 or self.sprite.bottom > HEIGHT:
                self.direction = random.choice(["horizontal", "vertical", "diagonal"])

    def animate(self):
        self.timer += 1
        if self.timer % 15 == 0:
            self.index = (self.index + 1) % 2
            self.sprite.image = self.images[self.index]

    def draw(self):
        self.sprite.draw()


def draw_menu():
    screen.clear()
    background.draw()
    screen.draw.text("Squid Game", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color="white")
    start_button.draw()
    music_button.draw()
    quit_button.draw()


def draw_character_select():
    screen.clear()
    background.draw()
    screen.draw.text("Select Your Hero", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color="white")
    hero_1_button.draw()
    hero_2_button.draw()
    quit_button.draw()


def draw_game_over():
    screen.clear()
    background.draw()
    screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color="red")
    restart_button.draw()
    music_button.draw()
    quit_button.draw()


def draw_won():
    screen.clear()
    background.draw()
    screen.draw.text("You Won!", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color="green")
    restart_button.draw()
    music_button.draw()
    quit_button.draw()


def update():
    global game_state, time_left, enemies, hero

    if game_state == "character_select":
        pass

    elif game_state == "playing":
        time_left -= 1 / 60
        if time_left <= 0:
            game_state = "won"

        hero.move()
        hero.animate()

        if hero.idle_timer >= 180:
            sounds.game_over_sound.play()
            game_state = "game_over"

        for enemy in enemies[:]:
            enemy.move()
            enemy.animate()
            if hero.sprite.colliderect(enemy.sprite):
                hero.health -= enemy.damage
                enemy.health -= 10
                sounds.hit_sound.play()
                if hero.health <= 0:
                    sounds.game_over_sound.play()
                    game_state = "game_over"
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    if not enemies:
                        game_state = "won"
                        time_left = 0
        if keyboard.escape:
            game_state = "menu"

    elif game_state == "menu":
        draw_menu()

    elif game_state == "game_over":
        draw_game_over()

    elif game_state == "won":
        draw_won()


def on_mouse_down(pos):
    global game_state, music_playing, hero

    if game_state == "menu":
        if start_button.is_clicked(pos):
            game_state = "character_select"
        elif quit_button.is_clicked(pos):
            exit()

    elif game_state == "character_select":
        if hero_1_button.is_clicked(pos):
            hero = Hero(character="hero_1")
            reset_game()
        elif hero_2_button.is_clicked(pos):
            hero = Hero(character="hero_2")
            reset_game()
        elif quit_button.is_clicked(pos):
            exit()

    elif game_state in ["game_over", "won"]:
        if restart_button.is_clicked(pos):
            reset_game()
        elif quit_button.is_clicked(pos):
            exit()

    if music_button.is_clicked(pos):
        music_playing = not music_playing
        if music_playing:
            music.play("background_music")
            music_button.image = "music_on"
        else:
            music.stop()
            music_button.image = "music_off"


def reset_game():
    global game_state, time_left, hero, enemies
    game_state = "playing"
    time_left = 20
    hero.health = 100

    enemy_1_count = random.randint(3, 6)
    enemy_2_count = enemy_count - enemy_1_count

    enemies = []
    enemies += [Enemy(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), "enemy_1") for _ in range(enemy_1_count)]
    enemies += [Enemy(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), "enemy_2") for _ in range(enemy_2_count)]


def draw():
    screen.clear()
    background.draw()
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        hero.draw()
        for enemy in enemies:
            enemy.draw()
        screen.draw.text(f"Time Left: {int(time_left)}", (10, 40), fontsize=30, color="white")
    elif game_state == "game_over":
        draw_game_over()
    elif game_state == "won":
        draw_won()
    elif game_state == "character_select":
        draw_character_select()


pgzrun.go()
