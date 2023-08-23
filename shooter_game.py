#Создай собственный Шутер!

from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player (GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_widht - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

win_widht = 700
win_height = 600
display.set_mode((win_widht, win_height))
window = display.set_mode((win_widht, win_height))
background = transform.scale(image.load(img_back), (win_widht, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

font.init()
font2 = font.SysFont("Arial", 36)

score = 0
lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_widht - 80)
            self.rect.y = 0
            lost = lost + 1
fire_sound = mixer.Sound('fire.ogg')
img_bullet = "bullet.png"
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

img_enemy = 'ufo.png'
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_widht - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
bullets = sprite.Group()
max_lost = 3
goal = 10
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background,(0,0))

        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        ship.reset()
        monsters.update()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_widht - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

            if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
                finish = True
                window.blit(lose, (200, 200))

            if score >= goal:
                finish = True
                window.blit(win, (200, 200))

            text = font2.render("Счёт: " + str(score), 1, (255, 255, 255))
            window.blit(text, (10, 20))    

            text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
            window.blit(text_lose, (10, 50))

        display.update()

    time.delay(50)
