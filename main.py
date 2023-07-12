import pygame, sys, random
# from pygame import button

pygame.init()
clock=pygame.time.Clock()
screen=pygame.display.set_mode((600,380))
background=pygame.image.load("assets/bg.jpg")
pygame.mouse.set_visible(False)

class Button():
  def __init__(self,x,y,image,scale):
    width=image.get_width()
    height=image.get_height()
    self.image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
    self.rect=self.image.get_rect()
    self.rect.topleft=(x,y)
    self.clicked=False
  def draw(self,surface):
    action=False
    pos=pygame.mouse.get_pos()
    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
        self.clicked=True
        action=True
    if pygame.mouse.get_pressed()[0]==0:
      self.clicked=False
    surface.blit(self.image,(self.rect.x,self.rect.y)) 
    return action
  
exitImage=pygame.image.load("assets/button_images/exit_btn.png").convert_alpha()
startImage=pygame.image.load("assets/button_images/start_btn.png").convert_alpha()
start_button=Button(530,10,startImage,0.2)
exit_button=Button(530,350,exitImage,0.2)

class Crosshair(pygame.sprite.Sprite):
  def __init__(self, picture_path):
    super().__init__()
    self.image = pygame.image.load(picture_path)
    self.rect = self.image.get_rect()
  def update(self):
    self.rect.center = pygame.mouse.get_pos()

class Hitbox(pygame.sprite.Sprite):
  def __init__ (self,picture_path):
    super().__init__()
    self.image=pygame.image.load(picture_path)
    self.rect=self.image.get_rect()
    self.gunshot = pygame.mixer.Sound("assets/gunshot.wav")
  def shoot(self):
    self.gunshot.play()
    pygame.sprite.spritecollide(hitbox,target_group,True)
  def update(self):
    self.rect.center=pygame.mouse.get_pos()

class Target(pygame.sprite.Sprite):
  def __init__(self, picture_path, pos_x, pos_y):
    super().__init__()
    self.image = pygame.image.load(picture_path)
    self.rect = self.image.get_rect()
    self.rect.center = [pos_x, pos_y]

class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"assets/explosion_images/exp{num}.png")
			img = pygame.transform.scale(img, (50, 50))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 4
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()

target_group = pygame.sprite.Group()

hitbox = Hitbox("assets/target_images/hitbox.jpg")
hitbox_group = pygame.sprite.Group()
hitbox_group.add(hitbox)

explosion_group = pygame.sprite.Group()

crosshair=Crosshair("assets/target_images/crosshair.png")
crosshair_group=pygame.sprite.Group()
crosshair_group.add(crosshair)

target_group=pygame.sprite.Group()
for target in range(15):
  new_target=Target("assets/target_images/target.png",random.randrange(50,550),random.randrange(50,350))
  target_group.add(new_target)

run=True

while run:

  clock.tick(60)
  explosion_group.draw(screen)
  explosion_group.update()
  
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
     run=False
      
    if event.type==pygame.MOUSEBUTTONDOWN:
      pos=pygame.mouse.get_pos()
      explosion=Explosion(pos[0],pos[1])
      explosion_group.add(explosion)
      print("shoot")
      hitbox.shoot()      
      
  pygame.display.update()
  screen.blit(background,(0,0))
  target_group.draw(screen)

  start_button.draw(screen)
  exit_button.draw(screen)
  crosshair_group.draw(screen)
  crosshair_group.update()
  hitbox_group.update()
  clock.tick(60)
pygame.quit()