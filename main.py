# Author: poinl
# Old Tetris cover I did. Completly free to use.

import pygame
import os
import random

img_dir = os.path.join(os.path.dirname(__file__), 'img')
snd_dir = os.path.join(os.path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600

POWERUP_TIME = 5000

FPS = 60

# colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First_Game")


explosive_anim = {}
explosive_anim["lg"] = []
explosive_anim["sm"] = []
explosive_anim["player"] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (45, 45))
    explosive_anim["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img , (25, 25))
    explosive_anim["sm"].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosive_anim["player"].append(img)


powerup_images = {}
powerup_images['shield'] = pygame.image.load(os.path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(os.path.join(img_dir, 'bolt_gold.png')).convert()


background = pygame.image.load(os.path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()

shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'pew.wav'))
shoot_sound.set_volume(0.2)
explosive_sounds = []

for sound in ['expl3.wav', 'expl6.wav']:
    explosive_sound = pygame.mixer.Sound(os.path.join(snd_dir, sound))
    explosive_sound.set_volume(0.2)
    explosive_sounds.append(explosive_sound)
pygame.mixer.music.load(os.path.join(snd_dir, 'Twister Tetris.mp3'))
pygame.mixer.music.set_volume(0.1)

player_img = pygame.image.load(os.path.join(img_dir, 'DurrrSpaceShip.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 25))
player_mini_img.set_colorkey(BLACK)
meteor_img = pygame.image.load(os.path.join(img_dir, 'Asteroid2.png')).convert()
bullet_img = pygame.image.load(os.path.join(img_dir, 'bullet.png')).convert()


class Mob (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = meteor_img
        self.image_orig = pygame.transform.scale(meteor_img, (40, 40))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rotate()
        if self.rect.top > HEIGHT + 10 or self.rect.right > WIDTH + 20 or self.rect.left < -25:
             self.rect.x = random.randrange(WIDTH - self.rect.width)
             self.rect.y = random.randrange(-100, -40)
             self.speedx = random.randrange(-3, 3)
             self.speedy = random.randrange(1, 8)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion (pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosive_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosive_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosive_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Bullet (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()


class Player (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 2
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if keystate[pygame.K_SPACE]:
            self.shoot()

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()



font_name = pygame.font.match_font("helvetica")

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_shield(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LEGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LEGTH
    outline_rect = pygame.Rect(x, y, BAR_LEGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Shoot them ALL!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False



game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

clock = pygame.time.Clock()

player = Player()

mobs = pygame.sprite.Group()
powerups = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

all_sprites.add(player)

for i in range(6):
    newmob()

score = 0
pygame.mixer.music.play(loops=-1)
game_over = True
run = True

while run:

    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 20
        expl = Explosion(hit.rect.center, "sm")
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_expl = Explosion(player.rect.center, "player")
            all_sprites.add(death_expl)
            player.hide()
            player.lives -= 1
            player.shield = 100

    if player.lives == 0 and not death_expl.alive():
        game_over = True

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)

    for hit in hits:
        score += 10
        random.choice(explosive_sounds).play()
        expl = Explosion(hit.rect.center, "lg")
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == "shield":
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        elif hit.type == "gun":
            player.powerup()

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 24, WIDTH / 2, 12)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    draw_shield(screen, 5, 5, player.shield)
    pygame.display.flip()


pygame.quit()
