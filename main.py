import pygame, random

class Target(pygame.sprite.Sprite):
  def __init__ (self,picture_path,pos_x,pos_y):
    super().__init__()
    self.image=pygame.image.load(picture_path)
    self.rect=self.image.get_rect()
    self.rect.center=[pos_x,pos_y]
      
class Hitbox(pygame.sprite.Sprite):
  def __init__ (self,picture_path):
    super().__init__()
    self.image=pygame.image.load(picture_path)
    self.rect=self.image.get_rect()
    self.gunshot = pygame.mixer.Sound("gunshot.wav")
  def shoot(self):
    self.gunshot.play()
    pygame.sprite.spritecollide(hitbox,target_group,True)
  def update(self):
    self.rect.center=pygame.mouse.get_pos()
      
class Crosshair(pygame.sprite.Sprite):
  def __init__ (self,picture_path):
    super().__init__()
    self.image=pygame.image.load(picture_path)
    self.rect=self.image.get_rect()
    
  def update(self):
    self.rect.center=pygame.mouse.get_pos()
    
pygame.init()
screen = pygame.display.set_mode((580, 409))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
background = pygame.image.load("bg.jpg")

target_group = pygame.sprite.Group()
for target in range(15):
  new_target = Target("target.png",random.randrange(10,590),random.randrange(10,390))
  target_group.add(new_target)

crosshair = Crosshair("crosshair.png")
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

hitbox = Hitbox("hitbox.jpg")
hitbox_group = pygame.sprite.Group()
hitbox_group.add(hitbox)
hitbox.shoot()

while True:
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      print("shoot")
      hitbox.shoot()

  pygame.display.flip()
  screen.blit(background,(0,0))
  target_group.draw(screen)
  crosshair_group.draw(screen)
  crosshair_group.update()

  hitbox_group.draw(screen)
  hitbox_group.update()

  clock.tick(60)