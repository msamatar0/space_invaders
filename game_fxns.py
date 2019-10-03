from game_objs import *
from game_sprites import *

def check_events(config, screen, stats, board, ship, aliens, bullets, button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown(config, screen, event, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup(config, screen, event, ship, bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_button \
                (config, screen, stats, board, ship, aliens, bullets, button, mouse_x, mouse_y)


def check_button \
                (config, screen, stats, board, ship, aliens, bullets, button, mouse_x, mouse_y):
    clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if clicked and not stats.game_active:
        config.init_speed()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        board.prep_score()
        board.prep_hs()
        board.prep_level()
        board.prep_ships()

        aliens.empty()
        bullets.empty()
        create_fleet(config, screen, ship, aliens)
        ship.center_ship()


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


def update_bullets \
                (config, screen, stats, board, ship, aliens, bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions \
        (config, screen, stats, board, ship, aliens, bullets)


def check_bullet_alien_collisions \
                (config, screen, stats, board, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += config.alien_pts * len(aliens)
        board.prep_score()
        check_high_score(stats, board)

    if len(aliens) == 0:
        bullets.empty()
        config.inc_speed()

        stats.level += 1
        board.prep_level()

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
    alien_width = alien.rect.width / 1.5
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number / 1.5
    aliens.add(alien)


def get_number_rows(config, ship_height, alien_height):
    available_space_y = (config.screen_height - \
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_fleet(config, screen, ship, aliens):
    alien = Alien(config, screen)
    number_aliens_x = get_number_aliens_x(config, alien.rect.width)
    number_rows = get_number_rows \
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


def ship_hit(config, screen, stats, board, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        board.prep_ships()
        aliens.empty()
        bullets.empty()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    create_fleet(config, screen, ship, aliens)
    ship.center_ship()

    sleep(0.5)


def place_bunkers(bunkers):
    bunker = Bunker


def check_aliens_bottom(config, screen, stats, board, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(config, screen, stats, board, ship, aliens, bullets)
            break


def update_aliens(config, screen, stats, board, ship, aliens, bullets):
    check_fleet_edges(config, aliens)
    aliens.update()

    check_aliens_bottom(config, screen, stats, board, ship, aliens, bullets)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(config, screen, stats, board, ship, aliens, bullets)


def check_high_score(stats, board):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        board.prep_hs()


def update_screen(config, screen, stats, board, ship, aliens, bullets, button):
    screen.fill(config.bg_color)
    ship.blitme()
    aliens.draw(screen)
    for bullet in bullets:
        bullet.draw()

    board.show()

    if not stats.game_active:
        button.draw()

    pygame.display.flip()