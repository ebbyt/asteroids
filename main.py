import os
import pygame as pg
import pygame.freetype
from random import choice, randint
from sprites import Asteroid, Spaceship, Laser, Button, PowerUp  
from setings import SCREEN_HIGHT, SCREEN_WIGHT, WHITE, VIOLET


def draw_menu():
    screen.fill(VIOLET)
    screen.blit(game_over_surf, game_over_rect)
    button.draw(screen)
    button_quit.draw(screen)
    screen.blit(hp_img, (20, 20))
    screen.blit(x_img, (60, 28))
    score_font.render_to(screen, (80, 23), str(ship.hp), WHITE)
    score_font.render_to(screen, (SCREEN_WIGHT-180, 23), str(ship.score).zfill(5), WHITE)

def check_ship_collision():
    if pg.sprite.spritecollide(ship, asteroid_group, True):
        ship_hit_sound.play()
        ship.get_damage(1)


def check_laser_collision():
    for laser in laser_group:
        if pg.sprite.spritecollide(laser, asteroid_group, True):
            meteor_hit_sound.play()
            laser.kill()
            ship.score += 1


def check_power_up_collision():
    power_up = pg.sprite.spritecollideany(ship, power_up_group)
    if power_up == None:
        return
    if power_up.type == 'shield':
        ship.apply_shield()
        power_up.kill
    elif power_up.type == 'bolt':
        ship.apply_speed()
        power_up.kill


def draw_game():
    screen.blit(background_img, (0, 0))
    ship.draw(screen)
    laser_group.draw(screen)
    asteroid_group.draw(screen)
    power_up_group.draw(screen)
    screen.blit(hp_img, (20, 20))
    screen.blit(x_img, (60, 28))
    score_font.render_to(screen, (85, 23), str(ship.hp), WHITE)
    score_font.render_to(screen, (SCREEN_WIGHT-180, 23), str(ship.score).zfill(5), WHITE)


def update_game():
    ship.update()
    asteroid_group.update()
    laser_group.update()
    power_up_group.update()
    check_laser_collision()
    check_ship_collision()
    check_power_up_collision()


def make_laser():
    fire_laser_sound.play()
    laser_group.add(Laser(ship.rect.center, laser_img))


def make_metor():
    asteroid_img = choice(asteroid_imgs)
    asteroid = Asteroid((randint(0, SCREEN_WIGHT), -20), asteroid_img)
    asteroid_group.add(asteroid)


def make_power_up():
    random_number = randint(0, 100)
    pos = (randint(0, SCREEN_WIGHT), -20)
    if random_number % 2 == 0:
        power_up = PowerUp(pos, power_ups['shield'], 'shield')
        power_up_group.add(power_up)
    elif random_number % 3 == 0:
        power_up = PowerUp(pos, power_ups['bolt'], 'bolt')
        power_up_group.add(power_up)


def stop_game():
    pg.mouse.set_visible(True)
    background_music.fadeout(5000)
    laser_group.empty()
    asteroid_group.empty()
    

def restart_game():
    pg.mouse.set_visible(False)
    background_music.play(-1)
    new_game_sound.play()
    ship.rebuild()


pg.init()


ship_img = [pg.image.load(f'res\PNG\Damage\playerShip2_damage{i}.png') for i in range(1, 4)]
engine_imgs = [pg.image.load(f'res\PNG\Effects\\fire{h}.png') for h in range(1, 8) ]
ship_img.insert(0, pg.image.load('res\PNG\playerShip2_orange.png') )

power_ups = {'shield': pg.image.load('res\PNG\Power-ups\shield_silver.png'),
                'bolt': pg.image.load('res\PNG\Power-ups\\bold_silver.png')}
shield_imgs = [pg.image.load(f'res\PNG\Effects\shield{i}.png') for i in range(1, 4)]

background_img = pg.image.load('res\Backgrounds\\black.png')
background_img = pg.transform.scale(background_img, (SCREEN_WIGHT, SCREEN_HIGHT))
asteroid_imgs = [pg.image.load('res\PNG\Meteors\\'+ name) for name in os.listdir('res\PNG\Meteors')] 
laser_img = [pg.image.load(f'res\PNG\Lasers\laserRed{n}.png') for n in range(12, 17)]


hp_img = pg.image.load('res\PNG\\UI\playerLife2_orange.png')
x_img = pg.image.load('res\PNG\\UI\\numeralX.png')

fire_laser_sound = pg.mixer.Sound('res\Bonus\sfx_laser1.ogg')
meteor_hit_sound = pg.mixer.Sound('res\Bonus\meteor_hit.wav')
ship_hit_sound = pg.mixer.Sound('res\Bonus\hit.wav')
game_over_sound = pg.mixer.Sound('res\Bonus\sfx_lose.ogg')
new_game_sound = pg.mixer.Sound('res\Bonus\sfx_twoTone.ogg')
background_music = pg.mixer.Sound('res\Bonus\space_ambiance.wav')


clock = pg.time.Clock()
screen = pg.display.set_mode((SCREEN_WIGHT, SCREEN_HIGHT))
pg.display.set_caption('Meteor Vegas')
game_state = 'MAIN GAME'

score_font = pg.freetype.Font("res\Bonus\kenvector_future.ttf", 32)
text_font = pg.freetype.Font("res\Bonus\kenvector_future.ttf", 52)

button_quit = Button((SCREEN_WIGHT/2, SCREEN_HIGHT/2), 'quit', text_font)
button = Button((SCREEN_WIGHT/2, SCREEN_HIGHT/3), 'restart', text_font)
game_over_surf, game_over_rect = text_font.render('game over')
game_over_rect.center = (SCREEN_WIGHT/2, SCREEN_HIGHT/3)

ship = Spaceship((SCREEN_WIGHT/2, SCREEN_HIGHT-50), ship_img, engine_imgs, shield_imgs) 
asteroid_group = pg.sprite.Group()
laser_group = pg.sprite.GroupSingle()
power_up_group = pg.sprite.Group()


SPAWN_ASTEROID = pg.USEREVENT
pg.time.set_timer(SPAWN_ASTEROID, 500)

SPAWN_POWER_UP = pg.USEREVENT + 2 
pg.time.set_timer(SPAWN_POWER_UP, 1000)

background_music.play(-1)
running = True
pg.mouse.set_visible(False)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False 

        if game_state == 'MAIN GAME':
            if event.type == SPAWN_ASTEROID:
                make_metor()
            elif event.type == SPAWN_POWER_UP:
                make_power_up()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if len(laser_group) == 0:
                    make_laser()
            elif event.type == ship.DESTROY_EVENT:
                game_state = 'MENU'
                stop_game()
        else:
            if event.type == pg.MOUSEBUTTONDOWN and button.rect.collidepoint(event.pos):
                game_state = 'MAIN GAME'
                restart_game()
            if event.type == pg.MOUSEBUTTONDOWN and button_quit.rect.collidepoint(event.pos):
                pg.QUIT()


    if game_state == "MAIN GAME":
        draw_game()
        update_game()
    else:
        draw_menu()

    clock.tick(60)
    pg.display.flip()