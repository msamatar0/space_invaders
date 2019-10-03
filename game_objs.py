import sys, time, pygame
from pygame import *
from pygame.sprite import *
from time import sleep
from game_sprites import *

class Settings():
  def __init__(self):
    self.screen_width = 900
    self.screen_height = 600
    self.bg_color = (0, 0, 0)
    self.sprite_width = 50
    self.sprite_height = 50
    self.ship_speed = .7
    self.lives = 3
    self.bullet_limit = 4
    self.bullet_speed = .5
    self.bullet_width = 4
    self.bullet_height = 8
    self.bullet_color = (255, 255, 255)
    self.alien_speed = .3
    self.alien_pts = 10
    self.drop_speed = 10
    self.fleet_dir = 1
    self.speed_scale = 1.1
    self.score_scale = 1.5
    self.init_speed()

  def init_speed(self):
    self.ship_speed = 1
    self.bullet_speed = 1
    self.alien_speed = .5
    self.fleet_dir = 1

  def inc_speed(self):
    self.ship_speed *= self.speed_scale
    self.bullet_speed *= self.speed_scale
    self.alien_speed *= self.speed_scale
    self.alien_pts = int(self.alien_pts * self.score_scale)


class GameStats:
  def __init__(self, config):
    self.config = config
    self.reset_stats()
    self.game_active = False
    self.high_score = 0

  def reset_stats(self):
    self.ships_left = self.config.lives
    self.score = 0
    self.level = 1

  
class Button():
  def __init__(self, config, screen, msg):
    self.screen = screen
    self.screen_rect = screen.get_rect()

    self.width, self.height = 200, 50
    self.color = (255, 0, 0)
    self.text_color = (255, 255, 255)
    self.font = pygame.font.SysFont(None, 48)
    self.rect = pygame.Rect(0, 0, self.width, self.height)
    self.rect.center = self.screen_rect.center
    self.prep(msg)
  
  def prep(self, msg):
    self.msg_image = self.font.render\
      (msg, True, self.text_color, self.color)
    self.msg_image_rect = self.msg_image.get_rect()
    self.msg_image_rect.center = self.rect.center

  def draw(self):
    self.screen.fill(self.color, self.rect)
    self.screen.blit(self.msg_image, self.msg_image_rect)
