from game_fxns import *

config = Settings()

def run_game():
  pygame.init()
  pygame.mixer.init()
  screen = pygame.display.set_mode\
    ((config.screen_width, config.screen_height))
  pygame.display.set_caption("Space Invaders...?")

  button = Button(config, screen, "PLAY")
  stats = GameStats(config)
  ship = Ship(config, screen)
  bullets = Group()
  aliens = Group()
  alien_bullets = Group()
  bunkers = Group()
  ufo = Group()
  board = Scoreboard(config, screen, stats)

  place_bunkers(bunkers, config, screen)
  create_fleet(config, screen, ship, aliens)
  button.draw()
  update_screen\
        (config, screen, stats, board, ship, aliens, ufo, bunkers, bullets, alien_bullets, button)

  pygame.mixer.music.load('sound/theme.wav')
  pygame.mixer.music.play(-1)
  while True:
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
        (config, screen, stats, board, ship, aliens, ufo, bunkers, bullets, alien_bullets, button)

run_game()
