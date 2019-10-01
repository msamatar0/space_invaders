import sys, time, pygame
from pygame import *
from pygame.sprite import Sprite
from time import sleep
from game import *

class Ship():
  def __init__(self, screen, config):
    self.screen = screen
    self.config = config
    self.image = pygame.image.load('ship.bmp')
    self.rect = self.image.get_rect()
    self.screen_rect = screen.get_rect()
    self.rect.centerx = self.screen_rect.centerx
    self.rect.bottom = self.screen_rect.bottom
    self.center = float(self.rect.centerx)
    self.right = False
    self.left = False

  def update(self):
    if self.right and self.rect.right < self.screen_rect.right:
      self.center += self.config.speed
    if self.left and self.rect.left > 0:
      self.center -= self.config.speed

    self.rect.centerx = self.center

  def center_ship(self):
    self.center = self.screen_rect.centerx
    
  def blitme(self):
    self.screen.blit(self.image, self.rect)


class Bullet(Sprite):
  def __init__(self, config, screen, ship):
    super().__init__()
    self.screen = screen
    self.rect = pygame.Rect\
      (0, 0, config.bullet_width, config.bullet_height)
    self.rect.centerx = ship.rect.centerx
    self.rect.top = ship.rect.top
    self.y = float(self.rect.y)
    self.color = config.bullet_color
    self.speed = config.bullet_speed

  def update(self):
    self.y -= self.speed
    self.rect.y = self.y

  def draw(self):
    pygame.draw.rect(self.screen, self.color, self.rect)


class Alien(Sprite):
  def __init__(self, config, screen):
    super().__init__()
    self.screen = screen
    self.config = config
    self.image = pygame.image.load('alien.bmp')
    self.rect = self.image.get_rect()
    self.rect.x = self.rect.width
    self.rect.y = self.rect.height
    self.x = float(self.rect.x)
    self.speed = config.speed

  def blitme(self):
    self.screen.blit(self.image, self.rect)

  def update(self):
    self.x += (self.config.alien_speed * self.config.fleet_dir)
    self.rect.x = self.x

  def check_edges(self):
    screen_rect = self.screen.get_rect()
    if self.rect.right >= screen_rect.right:
      return True
    elif self.rect.left <= 0:
      return True
