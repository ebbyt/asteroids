import pygame as pg
from setings import SCREEN_HIGHT, SCREEN_WIGHT 


class Frog(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_animating = False
        self.sprites = [pg.image.load(f'frog\\attack_{n}.png') for n in range(1, 10)]
        self.frame = 0
        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect(center=(140, 140))

    def animation(self):
        self.is_animating = True

    def draw(self, target_surf):
        target_surf.blit(self.image, self.rect)

    def update(self, speed):
        if self.is_animating:
            self.frame += speed
            if int(self.frame) == len(self.sprites):
                self.frame = 0 
                self.is_animating = False

        self.image = self.sprites[int(self.frame)]

        

pg.init()
frog = Frog()
clock = pg.time.Clock()
screen = pg.display.set_mode((SCREEN_WIGHT, SCREEN_HIGHT))
pg.display.set_caption('Frog')

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False


        if event.type == pg.MOUSEBUTTONDOWN:
            frog.animation()
            
    screen.fill((120, 30, 50))    
    frog.update(0.25)
    frog.draw(screen)

    clock.tick(60)
    pg.display.flip()