import pygame as pg
from random import randint
from setings import SCREEN_HIGHT, SCREEN_WIGHT


class Spaceship:
    def __init__(self, pos, images, engine_images, shield_images) -> None:
        self.image = images[0]
        self.images = images
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hp = 4
        self.player_speed = 3
        self.score = 0
        self.start_pos = pos
        self.DESTROY_EVENT = pg.USEREVENT + 1
        self.frame = 0
        self.engine_images = engine_images
        self.engine_animation_len = len(engine_images)
        self.shield_power = 0
        self.shield_images = shield_images
        self.shield_rect = self.shield_images[0].get_rect()

    def draw_shield(self, target_pos):
        if self.shield_power > 0:
            self.shield_rect.center = self.rect.center
            if self.shield_power != 1:
                self.shield_rect.move_ip((-5, 5))
            target_pos.blit(self.shield_images[self.shield_power-1], self.shield_rect)

    def draw_engine_animation(self, target_pos):
        self.frame += 0.5
        if int(self.frame) == self.engine_animation_len:
            self.frame = 0
        img = self.engine_images[int(self.frame)]
        left_engine_pos = (self.rect.centerx-35, self.rect.bottom-18)
        right_engine_pos = (self.rect.centerx+21, self.rect.bottom-18)
        target_pos.blit(img, left_engine_pos)
        target_pos.blit(img, right_engine_pos)

    def draw(self, target_pos):
        if self.hp > 0:
            target_pos.blit(self.image, self.rect)
            if self.hp < 4:
                target_pos.blit(self.images[-self.hp], self.rect)
        self.draw_engine_animation(target_pos)
        self.draw_shield(target_pos)

    def update(self):
        self.move()
        self.resistens()

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.rect.y -= self.player_speed
        if keys[pg.K_s]:
            self.rect.y += self.player_speed
        if keys[pg.K_d]:
            self.rect.x += self.player_speed
        if keys[pg.K_a]:
            self.rect.x -= self.player_speed
    
    def get_damage(self, damage):
        if self.shield_power > 0:
            self.shield_power -= damage
        else:
            self.hp -= damage
            if self.hp <= 0:
                pg.event.post(pg.event.Event(self.DESTROY_EVENT))
                
    def resistens(self):
        if self.rect.right > SCREEN_WIGHT:
            self.rect.right = SCREEN_WIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HIGHT:
            self.rect.bottom = SCREEN_HIGHT

    def rebuild(self):
        self.hp = 4
        self.score = 0
        self.is_alive = True
        self.rect.center = self.start_pos

    def apply_shield(self):
        self.shield_power = 3

    def apply_speed(self):
        self.player_speed = 7

    
class Asteroid(pg.sprite.Sprite):
    def __init__(self, pos, image) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.speed_x = randint(-3, 3)
        self.speed_y = randint(3, 9)
        self.original_image = image
        self.angle = 0
        self.rotation_speed = randint(-3, 3)  

    def update(self):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HIGHT:
            self.kill()

    def rotate(self):
        self.angle += self.rotation_speed
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)



class Laser(pg.sprite.Sprite):
    def __init__(self, pos, images):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.animation_len = len(images)
        self.frame = 0
        self.rect = self.image.get_rect(center=pos)
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()
        self.frame += 0.25
        if int(self.frame) == self.animation_len:
            self.frame = 0
        self.image = self.images[int(self.frame)]


class Button():
    def __init__(self, pos, text, font):
        super().__init__()
        self.image = pg.Surface((450, 80))
        self.image.fill('#e09f23')
        self.rect = self.image.get_rect(center=pos)
        self.text_surf, self.text_rect = font.render(text, size=42)
        self.text_rect.center = self.rect.center
        
    def draw(self, target_surf):
        target_surf.blit(self.image, self.rect)
        target_surf.blit(self.text_surf, self.text_rect)


class PowerUp(pg.sprite.Sprite):
    def __init__(self, pos, image, _type) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.type = _type
        self.speed_y = randint(1,6)


    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()
