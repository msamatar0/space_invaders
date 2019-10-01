import sys, time, pygame
from pygame import *
from pygame.sprite import Sprite
from time import sleep

class Settings():
  def __init__(self):
    self.screen_width = 900
    self.screen_height = 600
    self.bg_color = (230, 230, 230)
    self.speed = .7
    self.lives = 3
    self.bullet_limit = 4
    self.bullet_speed = 3
    self.bullet_width = 3
    self.bullet_height = 8
    self.bullet_color = (255, 0, 0)
    self.alien_speed = 1
    self.drop_speed = 10
    self.fleet_dir = 1

class GameStats():
  def __init__(self, config):
    self.config = config
    self.reset_stats()
    self.game_active = True

  def reset_stats(self):
    self.ships_left = self.config.lives

def check_events(config, screen, ship, bullets):
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

      elif event.type == pygame.KEYDOWN:
        check_keydown(config, screen, event, ship, bullets)
      elif event.type == pygame.KEYUP:
        check_keyup(config, screen, event, ship, bullets)

  
def check_keydown(config, screen, event, ship, bullets):
  if event.key == pygame.K_q:
    sys.exit()
  elif event.key == pygame.K_RIGHT:
    ship.right = True
  elif event.key == pygame.K_LEFT:
    ship.left = True
  elif event.key == pygame.K_z:
    fire(config, screen, ship, bullets)


def check_keyup(config, screen, event, ship, bullets):
  if event.key == pygame.K_RIGHT:
    ship.right = False
  elif event.key == pygame.K_LEFT:
    ship.left = False


def update_screen(config, screen, ship, aliens, bullets):
  screen.fill(config.bg_color)
  ship.blitme()
  aliens.draw(screen)
  for bullet in bullets:
    bullet.draw()
  pygame.display.flip()


def update_bullets(config, screen, ship, aliens, bullets):
  bullets.update()
  

  for bullet in bullets.copy():
    if bullet.rect.bottom <= 0:
      bullets.remove(bullet)

  check_bullet_alien_collisions(config, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(config, screen, ship, aliens, bullets):
  collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

  if len(aliens) == 0:
    bullets.empty()
    create_fleet(config, screen, ship, aliens)


def fire(config, screen, ship, bullets):
  if len(bullets) < config.bullet_limit:
    new_bullet = Bullet(config, screen, ship)
    bullets.add(new_bullet)


def get_number_aliens_x(config, alien_width):
  available_space_x = config.screen_width - 2 * alien_width
  number_aliens_x = int(available_space_x / (2 * alien_width))
  return number_aliens_x


def create_alien(config, screen, aliens, alien_number, row_number):
  alien = Alien(config, screen)
  alien_width = alien.rect.width
  alien.x = alien_width + 2 * alien_width * alien_number  
  alien.rect.x = alien.x
  alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
  aliens.add(alien)


def get_number_rows(config, ship_height, alien_height):
  available_space_y = (config.screen_height -\
    (3 * alien_height) - ship_height)
  number_rows = int(available_space_y / (2 * alien_height))
  return number_rows


def create_fleet(config, screen, ship, aliens):
  alien = Alien(config, screen)
  number_aliens_x = get_number_aliens_x(config, alien.rect.width)
  number_rows = get_number_rows\
    (config, ship.rect.height, alien.rect.height)

  for row_number in range(number_rows):
    for alien_number in range(number_aliens_x):
      create_alien(config, screen, aliens, alien_number, row_number)


def check_fleet_edges(config, aliens):
  for alien in aliens.sprites():
    if alien.check_edges():
      change_dir(config, aliens)
      break


def change_dir(config, aliens):
  for alien in aliens.sprites():
    alien.rect.y += config.drop_speed

  config.fleet_dir *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
  if stats.ships_left > 0:
    stats.ships_left -= 1
    aliens.empty()
    bullets.empty()

  else:
    stats.game_active = False

  create_fleet(ai_settings, screen, ship, aliens)
  ship.center_ship()

  sleep(0.5)


def check_aliens_bottom(config, stats, screen, ship, aliens, bullets):
  screen_rect = screen.get_rect()
  for alien in aliens.sprites():
    if alien.rect.bottom >= screen_rect.bottom:
      ship_hit(config, stats, screen, ship, aliens, bullets)
      break

def update_aliens(config, stats, screen, ship, aliens, bullets):
  check_fleet_edges(config, aliens)
  aliens.update()

  check_aliens_bottom(config, stats, screen, ship, aliens, bullets)
  if pygame.sprite.spritecollideany(ship, aliens):
    ship_hit(config, stats, screen, ship, aliens, bullets)
