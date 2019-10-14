import sys, time, random, pygame
from pygame import *
from pygame.sprite import *
from time import sleep
from game_sprites import *


class Settings():
  def __init__(self):
    self.screen_width = 900
    self.screen_height = 600
    self.bg_color = (0, 0, 0)
    self.sprite_width = 40
    self.sprite_height = 34
    self.ship_speed = 1.2
    self.lives = 3
    self.bunker_hp = 8
    self.bullet_limit = 2
    self.bullet_speed = 2
    self.bullet_width = 4
    self.bullet_height = 8
    self.bullet_color = (255, 255, 255)
    self.alien_speed = .8
    self.alien_pts = 10
    self.drop_speed = 10
    self.fleet_dir = 1
    self.bunker_space = 90
    self.bunker_max = 4
    self.speed_scale = 1.2
    self.score_scale = 1.5
    self.init_speed()

  def init_speed(self):
    self.ship_speed = 1.4
    self.bullet_speed = 2.8
    self.alien_speed = 777.1
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
    self.game_exiting = False
    self.high_score = 0

  def reset_stats(self):
    self.ships_left = self.config.lives
    self.score = 0
    self.level = 1
    self.ufo_dir = 1

  
class Button():
  def __init__(self, config, screen, font, msg):
    self.screen = screen
    self.screen_rect = screen.get_rect()

    self.width, self.height = 120, 40
    self.color = (255, 0, 0)
    self.text_color = (255, 255, 255)
    self.font = font
    self.rect = pygame.Rect(0, 0, self.width, self.height)
    self.rect.center = self.screen_rect.center
    self.rect.y += 50
    self.prep(msg)
  
  def prep(self, msg):
    self.msg_image = self.font.render\
      (msg, True, self.text_color, self.color)
    self.msg_image_rect = self.msg_image.get_rect()
    self.msg_image_rect.center = self.rect.center

  def draw(self):
    self.screen.fill(self.color, self.rect)
    self.screen.blit(self.msg_image, self.msg_image_rect)


class Scoreboard:
  def __init__(self, config, screen, font, stats):
    self.screen = screen
    self.screen_rect = screen.get_rect()
    self.config = config
    self.stats = stats
    self.text_color = (255, 255, 255)
    self.font = font
    self.prep_score()
    self.prep_hs()
    self.prep_level()
    self.prep_ships()

  def prep_score(self):
    rounded_score = round(self.stats.score, -1)
    score_str = "{:,}".format(rounded_score)

    self.score_img = self.font.render\
      (score_str, True, self.text_color, self.config.bg_color)

    self.score_rect = self.score_img.get_rect()
    self.score_rect.right = self.screen_rect.right - 15
    self.score_rect.top = 15

  def prep_hs(self):
    high_score = round(self.stats.high_score, -1)
    high_score_str = "{:,}".format(high_score)
    self.high_score_image = self.font.render\
      (high_score_str, True, self.text_color, self.config.bg_color)

    self.high_score_rect = self.high_score_image.get_rect()
    self.high_score_rect.centerx = self.screen_rect.centerx
    self.high_score_rect.top = self.score_rect.top

  def prep_level(self):
    self.level_image = self.font.render\
      (str(self.stats.level), True, self.text_color, self.config.bg_color)
    self.level_rect = self.level_image.get_rect()
    self.level_rect.right = self.score_rect.right
    self.level_rect.top = self.score_rect.bottom + 10

  def prep_ships(self):
    self.ships = Group()
    for ship_number in range(self.stats.ships_left):
      ship = Ship(self.config, self.screen)
      ship.image = pygame.transform.scale((pygame.image.load('images/ship.png')),\
      (int(self.config.sprite_width / 2),\
        int(self.config.sprite_height / 2)))
      ship.rect.x = 10 + ship_number * ship.rect.width
      ship.rect.y = 10
      self.ships.add(ship)

  def show(self):
    self.screen.blit(self.score_img, self.score_rect)
    self.screen.blit(self.high_score_image, self.high_score_rect)
    self.screen.blit(self.level_image, self.level_rect)
    self.ships.draw(self.screen)
