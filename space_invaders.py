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
  board = Scoreboard(config, screen, stats)

  create_fleet(config, screen, ship, aliens)
  place_bunkers(bunkers, config, screen)
  button.draw()
  update_screen\
        (config, screen, stats, board, ship, aliens, bunkers, bullets, button)

  while True:
    check_events\
      (config, screen, stats, board, ship, aliens, bullets, button)
    if stats.game_active:
      ship.update()
      update_bullets\
        (config, screen, stats, board, ship, aliens, bunkers, bullets)
      update_aliens\
        (config, screen, stats, board, ship, aliens, bullets)
      update_screen\
        (config, screen, stats, board, ship, aliens, bunkers, bullets, button)

run_game()
