import pygame as pg
from random import randint
from setings import SCREEN_HIGHT, SCREEN_WIGHT


class Spaceship:
    def __init__(self, pos, images) -> None:
        self.image = images[0]
        self.images = images
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hp = 4
    

    def draw(self, target_pos):
        if self.hp > 0:
            target_pos.blit(self.image, self.rect)
            if self.hp < 4:
                target_pos.blit(self.images[-self.hp], self.rect)

    def update(self):
        self.move()
        self.resistens()


    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.rect.y -= 5
        if keys[pg.K_s]:
            self.rect.y += 5
        if keys[pg.K_d]:
            self.rect.x += 5
        if keys[pg.K_a]:
            self.rect.x -= 5
    
    
    def get_damage(self, damage):
        if self.hp > 0:
            self.hp -= damage

    def resistens(self):
        if self.rect.right > SCREEN_WIGHT:
            self.rect.right = SCREEN_WIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HIGHT:
            self.rect.bottom = SCREEN_HIGHT

    


class Asteroid(pg.sprite.Sprite):
    def __init__(self, pos, image) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.speed_x = randint(-3, 3)
        self.speed_y = randint(3, 9)  

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HIGHT:
            self.kill()


class Laser(pg.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()