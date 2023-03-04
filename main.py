import pygame, sys, random
pygame.init()
clock=pygame.time.Clock()
screen=pygame.display.set_mode((600,400))
background=pygame.image.load("backgroundimage.jpg")
while True:
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type==pygame.MOUSEBUTTONDOWN:
      print("shoot")
  pygame.display.flip()
  screen.blit(background,(0,0))
  clock.tick(60)