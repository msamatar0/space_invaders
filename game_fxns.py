from game_objs import *
from game_sprites import *

def check_events(config, screen, stats, board, ship, aliens, bunkers, ufo, bullets, button):
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
                (config, screen, stats, board, ship, aliens, bunkers, bullets, button, mouse_x, mouse_y)


def check_button \
                (config, screen, stats, board, ship, aliens, bunkers, bullets, button, mouse_x, mouse_y):
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
        place_bunkers(bunkers, config, screen)


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
                (config, screen, stats, board, ship, aliens, ufo, bunkers, bullets, alien_bullets):
    bullets.update()
    alien_bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions\
        (config, screen, stats, board, ship, aliens, bullets)

    check_bunker_bullet_collisions\
        (config, bullets, bunkers)

    check_bunker_bullet_collisions\
        (config, alien_bullets, bunkers)

    check_bullet_ufo_collisions\
        (config, screen, stats, board, ufo, bullets)

def check_bullet_alien_collisions\
                (config, screen, stats, board, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score +=\
                config.alien_pts * aliens[0].type * len(aliens)
        board.prep_score()
        check_high_score(stats, board)

    if len(aliens) == 0:
        bullets.empty()
        config.inc_speed()

        stats.level += 1
        board.prep_level()

        create_fleet(config, screen, ship, aliens)



def check_bullet_ufo_collisions\
    (config, screen, stats, board, ufo, bullets):
    collisions = pygame.sprite.groupcollide(bullets, ufo, True, True)

    if collisions:
        for ufo in collisions.values():
            stats.score += random.radrange(50, 400, 50)

def fire(config, screen, ship, bullets):
    if len(bullets) < config.bullet_limit:
        new_bullet = Bullet(config, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(config, alien_width):
    available_space_x = config.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(config, screen, aliens, alien_number, row_number, alien_type):
    alien = Alien(config, screen, alien_type)
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
    alien = Alien(config, screen, 1)
    number_aliens_x = get_number_aliens_x(config, alien.rect.width)
    number_rows = get_number_rows\
        (config, ship.rect.height, alien.rect.height)

    alien_type = 0

    for row_number in range(number_rows):
        if (row_number + 1) % 3 == 0:
            alien_type = 1
        elif (row_number + 1) % 3 == 2:
            alien_type = 2
        else:
            alien_type = 3
        for alien_number in range(number_aliens_x):
            create_alien\
                (config, screen, aliens, alien_number, row_number, alien_type)

def check_fleet_edges(config, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_dir(config, aliens)
            break


def change_dir(config, aliens):
    for alien in aliens.sprites():
        alien.rect.y += config.drop_speed

    config.fleet_dir *= -1


def ship_hit(config, screen, stats, board, ship, aliens, bunkers, bullets, alien_bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        board.prep_ships()
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    create_fleet(config, screen, ship, aliens)
    ship.center_ship()

    sleep(0.5)


def place_bunkers(bunkers, config, screen):
    offset = 120
    for i in range(config.bunker_max):
        interval =\
            (i + 1) * (config.screen_width / config.bunker_max) - offset
        bunker = Bunker(config, screen)
        bunker.rect.x = interval - bunker.rect.width / 2
        bunker.rect.y = config.screen_height - offset * 1.1
        bunkers.add(bunker)


def check_bunker_bullet_collisions(config, bullets, bunkers):
    collisions = pygame.sprite.groupcollide(bullets, bunkers, True, False)

    if collisions:
        for bullets in collisions:
            for bunker in collisions.get(bullets):
                if bunker.hp <= 0:
                    bunkers.remove(bunker)
                else:
                    bunker.hp -= 1

def check_aliens_bottom(config, screen, stats, board, ship, aliens, bunkers, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(config, screen, stats, board, ship, aliens, bunkers, bullets)
            break


def update_aliens\
    (config, screen, stats, board, ship, aliens, bunkers, bullets, alien_bullets):
    check_fleet_edges(config, aliens)
    aliens.update()
    alien_bullets.update()

    for alien in aliens:
        roll = random.randrange(1, 20001)
        
        if roll > 19998:
            shot = Alien_Fire(config, screen, alien)
            alien_bullets.add(shot)


    check_aliens_bottom(config, screen, stats, board, ship, aliens, bunkers, bullets)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(config, screen, stats, board, ship, aliens, bunkers, bullets, alien_bullets)
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(config, screen, stats, board, ship, aliens, bunkers, bullets, alien_bullets)


def update_ufo(config, screen, stats, ufo):
    roll = random.randrange(1, 201)

    if roll > 195 and ufo.empty():
        new_ufo = UFO(config, screen, stats.ufo_dir)
        stats.ufo_dir *= -1
        new_ufo.rect.y = 20
        new_ufo.rect.x =\
            -50 if status.ufo_dir else 50 + config.screen_width
        ufo.add(new_ufo)
        print("new ufo")

        ufo.update()


def check_high_score(stats, board):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        board.prep_hs()


def update_screen\
    (config, screen, stats, board, ship, aliens, ufo, bunkers, bullets, alien_bullets, button):
    screen.fill(config.bg_color)
    ship.blitme()
    aliens.draw(screen)

    for ufo_spawn in ufo:
        ufo_spawn.blitme()

    for bunker in bunkers:
        bunker.blitme()

    for bullet in bullets:
        bullet.draw()

    for bullet in alien_bullets:
        bullet.draw()

    board.show()

    if not stats.game_active:
        button.draw()

    pygame.display.flip()