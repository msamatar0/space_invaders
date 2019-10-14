from game_objs import *

clock = pygame.time.Clock()

class Ship(Sprite):
  def __init__(self, config, screen):
    super(Ship, self).__init__()
    self.screen = screen
    self.config = config
    self.image = pygame.transform.scale((\
      pygame.image.load('images/ship.png')),\
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
    pygame.mixer.Channel(1).play(\
      pygame.mixer.Sound('sound/ship_shoot.wav'))

  def update(self):
    self.y -= self.speed
    self.rect.y = self.y

  def draw(self):
    pygame.draw.rect(self.screen, self.color, self.rect)


class Alien_Fire(Sprite):
  def __init__(self, config, screen, alien):
    super().__init__()
    self.screen = screen
    self.rect = pygame.Rect\
      (0, 0, config.bullet_width, config.bullet_height)
    self.rect.centerx = alien.rect.centerx
    self.rect.top = alien.rect.top
    self.y = float(self.rect.y)
    self.color = config.bullet_color
    self.speed = config.bullet_speed - 1
    pygame.mixer.Channel(2).play(\
      pygame.mixer.Sound('sound/alien_shoot.wav'))

  def update(self):
    self.y += self.speed
    self.rect.y = self.y

  def draw(self):
    pygame.draw.rect(self.screen, self.color, self.rect)

class Alien(Sprite):
  def __init__(self, config, screen, alien_type):
    super().__init__()
    self.screen = screen
    self.config = config
    self.type = alien_type
    self.images = []
    self.frame = 0
    self.images.append(\
      pygame.transform.scale((pygame.image.load(\
        'images/alien' + str(alien_type) + '-1.png')),\
      (config.sprite_width, config.sprite_height)))
    self.images.append(\
      pygame.transform.scale((pygame.image.load(\
        'images/alien' + str(alien_type) + '-2.png')),\
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
  def __init__(self, config, screen, dir):
    super().__init__()
    self.config = config
    self.screen = screen
    self.images = []
    self.frame = 0
    self.images.append(\
      pygame.transform.scale((pygame.image.load(\
        'images/ufo-1.png')),\
      (config.sprite_width, config.sprite_height)))
    self.images.append(\
      pygame.transform.scale((pygame.image.load(\
        'images/ufo-2.png')),\
      (config.sprite_width, config.sprite_height)))
    self.image = self.images[self.frame]
    self.rect = self.image.get_rect()
    self.rect.x = self.rect.width
    self.rect.y = self.rect.height
    self.x = float(self.rect.x)
    self.speed = config.alien_speed
    self.dir = 1

  def update(self):
    self.x += (self.speed * self.dir)
    self.rect.x = self.x
    if self.rect.x % 20 == 0:
      self.frame = (self.frame + 1) % len(self.images)
      self.image = self.images[self.frame]

  def blitme(self):
    self.screen.blit(self.image, self.rect)

class Bunker(Sprite):
  def __init__(self, config, screen):
    super().__init__()
    self.config = config
    self.screen = screen
    self.image = pygame.transform.scale((pygame.image.load('images/bunker.png')),\
      (config.sprite_width + 70, config.sprite_height + 25))
    self.rect = self.image.get_rect()
    self.rect.x = self.rect.width
    self.rect.y = self.rect.height
    self.screen_rect = screen.get_rect()
    self.rect.centerx = self.screen_rect.centerx
    self.rect.bottom = self.screen_rect.bottom
    self.hp = 8

  def blitme(self):
    self.screen.blit(self.image, self.rect)
