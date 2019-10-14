from game_fxns import *

config = Settings()

def run_game():
  pygame.init()
  pygame.mixer.init()
  font = pygame.font.Font("PressStart2P.ttf", 16)

  screen = pygame.display.set_mode\
    ((config.screen_width, config.screen_height))
  screen_rect = screen.get_rect()
  pygame.display.set_caption("Space Invaders...?")
  icon = pygame.display.set_icon(\
    pygame.image.load('images/ship.png'))

  button = Button(config, screen, font, "PLAY")
  stats = GameStats(config)
  ship = Ship(config, screen)
  bullets = Group()
  aliens = Group()
  alien_bullets = Group()
  bunkers = Group()
  ufo = Group()
  board = Scoreboard(config, screen, font, stats)

  button.draw()
  
  title_1 = font.render\
    ("SPACE", True, board.text_color, config.bg_color)
  title_2 = font.render\
    ("INVADERS", True, board.text_color, config.bg_color)
  
  while True:
    update_screen\
      (config, screen, stats, board, ship, aliens, ufo, bunkers, bullets, alien_bullets, button, False)
    if check_events\
      (config, screen, stats, board, ship, aliens, bunkers, ufo, bullets, button):
      break
    
  place_bunkers(bunkers, config, screen)
  create_fleet(config, screen, ship, aliens)

  update_screen\
    (config, screen, stats, board, ship, aliens, ufo, bunkers, bullets, alien_bullets, button, True)
  pygame.mixer.music.load('sound/theme.wav')
  pygame.mixer.music.play(-1)
  while not stats.game_exiting:
    check_events\
      (config, screen, stats, board, ship, aliens, bunkers, ufo, bullets, button)
    if stats.game_active:
      ship.update()
      update_bullets\
        (config, screen, stats, board, ship, aliens, ufo, bunkers, bullets, alien_bullets)
      update_aliens\
        (config, screen, stats, board, ship, aliens, bunkers, bullets, alien_bullets)
      update_ufo\
        (config, screen, stats, ufo)
      update_screen\
        (config, screen, stats, board, ship, aliens, ufo, bunkers, bullets, alien_bullets, button, True)

run_game()
