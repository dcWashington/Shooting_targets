import pygame, random, time

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 380
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

background=pygame.image.load("assets/bg.jpg")
pygame.display.set_caption("Shooting Targets Game")

start_time = None
total_time = 30

in_menu = True
font = pygame.font.Font(None, 35)
play_option = font.render("Play", True, (255, 255, 255))
quit_option = font.render("Quit", True, (255, 255, 255))
play_rect = play_option.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
quit_rect = quit_option.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

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
        print("start clicked")

    if pygame.mouse.get_pressed()[0]==0:
      self.clicked=False
    surface.blit(self.image,(self.rect.x,self.rect.y)) 
    return action
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
    pygame.mixer.init()
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
			img = pygame.transform.scale(img, (30, 30))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 9
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()

startImage=pygame.image.load("assets/button_images/start_btn.png").convert_alpha()
start_button=Button(280,180,startImage,0.2)

hitbox = Hitbox("assets/target_images/hitbox.jpg")
hitbox_group = pygame.sprite.Group()
hitbox_group.add(hitbox)

explosion_group = pygame.sprite.Group()

crosshair=Crosshair("assets/target_images/crosshair.png")
crosshair_group=pygame.sprite.Group()
crosshair_group.add(crosshair)

target_group = pygame.sprite.Group()
target_group=pygame.sprite.Group()

for target in range(30):
  new_target=Target("assets/target_images/target.png",random.randrange(50,550),random.randrange(50,350))
  target_group.add(new_target)

run=True
while run:

  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      run=False
      
    if event.type == pygame.MOUSEBUTTONDOWN:  
      pos=pygame.mouse.get_pos()
      explosion=Explosion(pos[0],pos[1])
      explosion_group.add(explosion)
      print("shoot")
      hitbox.shoot()

      if in_menu:
        if play_rect.collidepoint(event.pos):
          in_menu = False
          start_time = time.time()
        elif quit_rect.collidepoint(event.pos):
            running = False       

  if in_menu:
    # Main Menu
    screen.fill((0, 0, 0))
    screen.blit(play_option, play_rect)
    screen.blit(quit_option, quit_rect)
    pygame.display.flip()

  else:
    # In-game
    pygame.mouse.set_visible(False)

    screen.blit(background,(0,0))
    target_group.draw(screen)

    crosshair_group.draw(screen)
    crosshair_group.update()
    hitbox_group.update()

    explosion_group.draw(screen)
    explosion_group.update()
    
    # Check for game over
    elapsed_time = time.time() - start_time if start_time else 0
    time_left = max(total_time - int(elapsed_time), 0)
    if time_left == 0:
      run = False

  # Display the timer
    timer_text = font.render("Time Left: " + str(time_left), True, "red")
    screen.blit(timer_text, (10, 10))

    pygame.display.flip()
pygame.quit()