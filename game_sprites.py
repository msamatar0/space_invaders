from game_objs import *

clock = pygame.time.Clock()

class Ship(Sprite):
  def __init__(self, config, screen):
    super(Ship, self).__init__()
    self.screen = screen
    self.config = config
    self.image = pygame.transform.scale((pygame.image.load('ship.png')),\
      (config.sprite_width, config.sprite_height))
    self.rect = self.image.get_rect()
    self.screen_rect = screen.get_rect()
    self.rect.centerx = self.screen_rect.centerx
    self.rect.bottom = self.screen_rect.bottom
    self.center = float(self.rect.centerx)
    self.right = False
    self.left = False

  def update(self):
    if self.right and self.rect.right < self.screen_rect.right:
      self.center += self.config.ship_speed
    if self.left and self.rect.left > 0:
      self.center -= self.config.ship_speed

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
  def __init__(self, config, screen, alien_type):
    super().__init__()
    self.screen = screen
    self.config = config
    self.images = []
    self.frame = 0
    self.images.append(\
      pygame.transform.scale((pygame.image.load(\
        'alien' + str(alien_type) + '-1.png')),\
      (config.sprite_width, config.sprite_height)))
    self.images.append(\
      pygame.transform.scale((pygame.image.load(\
        'alien' + str(alien_type) + '-2.png')),\
      (config.sprite_width, config.sprite_height)))
    self.image = self.images[self.frame]
    self.rect = self.image.get_rect()
    self.rect.x = self.rect.width
    self.rect.y = self.rect.height
    self.x = float(self.rect.x)
    self.speed = config.alien_speed

  def blitme(self):
    self.screen.blit(self.image, self.rect)

  def update(self):
    self.x += (self.config.alien_speed * self.config.fleet_dir)
    self.rect.x = self.x
    if self.rect.x % 20 == 0:
      self.frame = (self.frame + 1) % len(self.images)
      self.image = self.images[self.frame]

  def check_edges(self):
    screen_rect = self.screen.get_rect()
    if self.rect.right >= screen_rect.right:
      return True
    elif self.rect.left <= 0:
      return True


class UFO(Sprite):
  def __init__(config, screen):
    super().__init__()
    self.config = config
    self.screen = screen


class Bunker(Sprite):
  def __init__(self, config, screen):
    super().__init__()
    self.config = config
    self.screen = screen
    self.image = pygame.transform.scale((pygame.image.load('bunker.png')),\
      (config.sprite_width + 60, config.sprite_height + 26))
    self.rect = self.image.get_rect()
    self.screen_rect = screen.get_rect()
    self.rect.centerx = self.screen_rect.centerx
    self.rect.bottom = self.screen_rect.bottom
    self.hp = 8

  def blitme(self):
    self.screen.blit(self.image, self.rect)

    
class Scoreboard:
  def __init__(self, config, screen, stats):
    self.screen = screen
    self.screen_rect = screen.get_rect()
    self.config = config
    self.stats = stats
    self.text_color = (115, 115, 115)
    self.font = pygame.font.SysFont(None, 48)
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
      ship.image = pygame.transform.scale((pygame.image.load('ship.png')),\
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
