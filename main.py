import os
import pygame as pg
from random import choice, randint
from sprites import Asteroid, Spaceship, Laser  
from setings import SCREEN_HIGHT, SCREEN_WIGHT


ship_img = [pg.image.load(f'res\PNG\Damage\playerShip2_damage{i}.png') for i in range (1,4)]
ship_img.insert(0, pg.image.load('res\PNG\playerShip2_orange.png') )
background_img = pg.image.load('res\Backgrounds\\black.png')
background_img = pg.transform.scale(background_img, (SCREEN_WIGHT, SCREEN_HIGHT))
asteroid_imgs = [pg.image.load('res\PNG\Meteors\\'+ name) for name in os.listdir('res\PNG\Meteors')] 
laser_img = pg.image.load('res\PNG\Lasers\laserRed16.png')


pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((SCREEN_WIGHT, SCREEN_HIGHT))
pg.display.set_caption('Meteor Vegas')

ship = Spaceship((SCREEN_WIGHT/2, SCREEN_HIGHT-50), ship_img) 
asteroid_group = pg.sprite.Group()
laser_group = pg.sprite.GroupSingle()


SPAWN_ASTEROID = pg.USEREVENT
pg.time.set_timer(SPAWN_ASTEROID, 500)


running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False 

        if event.type == SPAWN_ASTEROID:
            asteroid_img = choice(asteroid_imgs)
            asteroid = Asteroid((randint(0, SCREEN_WIGHT), -20), asteroid_img)
            asteroid_group.add(asteroid)

        if event.type == pg.MOUSEBUTTONDOWN:
            if len(laser_group) == 0:
                laser_group.add(Laser(ship.rect.center, laser_img))

    if pg.sprite.spritecollide(ship, asteroid_group, True):
        ship.get_damage(1)
    
    for laser in laser_group:
        if pg.sprite.spritecollide(laser, asteroid_group, True):
            laser.kill()

    screen.blit(background_img, (0, 0))
    ship.draw(screen)
    laser_group.draw(screen)
    asteroid_group.draw(screen)

    ship.update()
    asteroid_group.update()
    laser_group.update()

    clock.tick(60)
    pg.display.flip()