import pygame
from pygame.locals import(RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,)
import random
import time

screenwidth = 1100
screenheight = 750
screen = pygame.display.set_mode((screenwidth,screenheight))
flags = 3
trans = (0, 0, 0, 0)
game_check = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self,pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1,0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenwidth:
            self.rect.right = screenwidth
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screenheight:
            self.rect.bottom = screenheight

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(screenwidth + 20, screenwidth + 100), random.randint(0, screenheight)))
        self.speed = random.randint(0, 2)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Meteorite(pygame.sprite.Sprite):
    def __init__(self):
        super(Meteorite, self).__init__()
        self.surf = pygame.image.load("meteorite.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(random.randint(screenwidth + 70, screenwidth + 100), random.randint(0, screenheight)))
        self.speed = random.randint(0, 1)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class FinishLine(pygame.sprite.Sprite):
    def __init__(self):
        super(FinishLine,self).__init__()
        self.surf = pygame.image.load("finishline.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(9900, 50))
        self.speed = random.randint(1, 1)

    def update(self):
        self.rect.move_ip(-self.speed, 0)



pygame.init()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 200)

ADDMETEORITE = pygame.USEREVENT + 2
pygame.time.set_timer(ADDMETEORITE, 500)

ADDFINISH = pygame.USEREVENT + 1

meteorite = pygame.sprite.Group()
enemies = pygame.sprite.Group()
finishline = pygame.sprite.Group()
player = Player()
finish = FinishLine()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(finish)
finishline.add(finish)

running = True
one=True
two=True
three=True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.type == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDMETEORITE:
            new_meteorite = Meteorite()
            meteorite.add(new_meteorite)
            all_sprites.add(new_meteorite)
    pressed_keys = pygame.key.get_pressed()
    if game_check == 1:

        player.update(pressed_keys)



        enemies.update()
        meteorite.update()
        finish.update()
        screen.fill((0,0,0))

        if one==True:
            live1 = pygame.image.load("heart.png")
            live1.set_colorkey((255, 255, 255), RLEACCEL)
            screen.blit(live1,(0, 0))

        if two == True:
            live2 = pygame.image.load("heart.png")
            live2.set_colorkey((255, 255, 255), RLEACCEL)
            screen.blit(live2,(100, 0))

        if three == True:
            live3 = pygame.image.load("heart.png")
            live3.set_colorkey((255, 255, 255), RLEACCEL)
            screen.blit(live3,(200, 0))



        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        col = pygame.sprite.spritecollideany(player, enemies)
        if col:
            col.kill()
            flags = flags - 1
            if flags == 2:
              three=False
            if flags == 1:
                two = False
            if flags == 0:
                one = False
                game_check = 0
        col2 = pygame.sprite.spritecollideany(player, meteorite)
        if col2:
            col2.kill()
            flags = flags - 1
            if flags == 2:
                three = False
            if flags == 1:
                two = False
            if flags == 0:
                one = False
                game_check = 0

        col3 = pygame.sprite.spritecollideany(player, finishline)
        if col3:
            game_check = 3


    elif game_check == 0:
        if pressed_keys[pygame.K_RSHIFT]:
            for s in all_sprites:
                s.kill()
            for e in enemies:
                e.kill()
            for m in meteorite:
                m.kill()
            for f in finishline:
                f.kill()
            all_sprites.add(player)
            all_sprites.add(finish)
            finishline.add(finish)
            finish.rect.x = screenwidth + 9900
            one = True
            two = True
            three = True
            flags = 3
            game_check = 1
        else:
            screen.fill((0, 0, 0))
            main_font = pygame.font.SysFont("Times", 80, True, False)
            main = main_font.render("!GAME OVER!", True, (218, 0, 0))
            text = pygame.font.SysFont("Times", 50, True, False)
            txt = text.render("Press the RIGHT SHIFT to play again", True, (255, 255, 255))
            screen.blit(main, (260, 225))
            screen.blit(txt, (150, 300))

    elif game_check == 3:
        if pressed_keys[pygame.K_RSHIFT]:
            for s in all_sprites:
                s.kill()
            for e in enemies:
                e.kill()
            for m in meteorite:
                m.kill()
            for l in finishline:
                l.kill()
                print(all_sprites)
            all_sprites.add(player)
            all_sprites.add(finish)
            finishline.add(finish)
            finish.rect.x = screenwidth + 9900
            one = True
            two = True
            three = True
            flags = 3
            game_check = 1
            print("running")
        else:
            screen.fill((0, 0, 0))
            main_font = pygame.font.SysFont("Times", 80, True, False)
            main = main_font.render("!YOU HAVE WON!", True, (0, 186, 0))
            text = pygame.font.SysFont("Times", 50, True, False)
            txt = text.render("Press the RIGHT SHIFT to play again", True, (255, 255, 255))
            screen.blit(main, (220, 225))
            screen.blit(txt, (150, 300))

    pygame.display.flip()

