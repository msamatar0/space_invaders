from game_fxns import *

config = Settings()

def run_game():
  pygame.init()
  screen = pygame.display.set_mode\
    ((config.screen_width, config.screen_height))
  pygame.display.set_caption("Alien Invasion!")

  button = Button(config, screen, "PLAY")
  stats = GameStats(config)
  ship = Ship(config, screen)
  bullets = Group()
  aliens = Group()
  bunkers = Group()
  ufo = Group()
  board = Scoreboard(config, screen, stats)

  place_bunkers(bunkers, config, screen)
  create_fleet(config, screen, ship, aliens)
  button.draw()
  update_screen\
        (config, screen, stats, board, ship, aliens, ufo, bunkers, bullets, button)

  while True:
    check_events\
      (config, screen, stats, board, ship, aliens, bunkers, ufo, bullets, button)
    if stats.game_active:
      ship.update()
      update_bullets\
        (config, screen, stats, board, ship, aliens, ufo, bunkers, bullets)
      update_aliens\
        (config, screen, stats, board, ship, aliens, bunkers, bullets)
      update_ufo\
        (config, screen, stats, ufo)
      update_screen\
        (config, screen, stats, board, ship, aliens, ufo, bunkers, bullets, button)

run_game()
