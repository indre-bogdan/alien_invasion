import sys
import pygame
from src.bullet import Bullet
from src.alien import Alien
from time import sleep

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event, ai_settings, screen, ship, bullets)
            elif event.type == pygame.KEYUP:
                check_keyup_events(event, ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y) 

def reset_ship_and_fleet(ai_settings, screen, ship, aliens, bullets):
    """Reset the ship and the fleet."""
    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
        
    # Create a new fleet and center the fleet.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
             
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Hide mouse.
        pygame.mouse.set_visible(False)
        
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        
        # Reset game statistics.
        stats.reset_stats()
        stats.game_active = True
        
        # Reset the scoreboard
        sb.prep_images()
        
        reset_ship_and_fleet(ai_settings, screen, ship, aliens, bullets)
                
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        
def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update the bullets and get rid of the old ones"""
    bullets.update()
        
    #Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)

def start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Start a new level"""
    bullets.empty()
    ai_settings.increase_speed()
        
    # Increase level
    stats.level += 1
    sb.prep_level()
        
    create_fleet(ai_settings, screen, ship, aliens)

def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collision"""
    # Check for any bullets that have hit aliens
    # if so, get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # If an entire fleet is destroyed, start a new level
        start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets)
         
def fire_bullet(ai_settings, screen, ship, bullets):
    """Creates a new bullet and fires it"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def end_game(stats, screen):
    """Ends the game and saves the high score."""
    
    # Save high score.
    try:
        with open('high_score.txt', 'r') as f:
            old_score = int(f.read())
    except FileNotFoundError:
        old_score = 0
    if stats.high_score > old_score:
        with open('high_score.txt', 'w') as f:
            f.write(str(stats.high_score))
    
    display_end_score(screen)
            
    # Set the game inactive.
    stats.game_active = False
    pygame.mouse.set_visible(True)
    
def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Respond to a ship being hit by alien.""" 
    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1
        
        # Update the scoreboard
        sb.prep_ships()
        
        reset_ship_and_fleet(ai_settings, screen, ship, aliens, bullets)
        
        # Pause.
        sleep(0.5)
    else:
        end_game(stats, screen)

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this as if the ship was hit
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break
    
def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Update the position of all aliens"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows to the ship"""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in a row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_number * alien_width
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    
    aliens.add(alien)
    
def create_fleet(ai_settings, screen, ship, aliens):
    """Creates a fleet of aliens"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    # Create fleet
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
        
def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break
   
def check_high_score(stats, sb):
    """Check to see if there is a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
   
def update_screen(ai_settings, screen, sb, ship, aliens, bullets):
    """Update images on the screen and flip to the new screen"""
 
    # Redraw the screen
    screen.fill(ai_settings.bg_color)
    
    # Redraw all the bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    # Draw the score information.
    sb.show_score()
    
    # Make the most recently drawn screen visible.
    pygame.display.flip()

def display_menu_screen(ai_settings, screen, stats, play_button):
    """Displays the menu screen."""
    
    # Draw the screen
    screen.fill(ai_settings.bg_color)
    
    play_button.draw_button()
    
    # Make the most recently drawn screen visible.
    pygame.display.flip()

def display_end_score(screen):
    """Displays the end score."""
    
    text_color = (30, 30, 30)
    font = pygame.font.SysFont(None, 60)
    text_image = font.render('GAME OVER', True, text_color)
    text_rect = text_image.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery - 100
    screen.blit(text_image, text_rect)
    
    # Make the most recently drawn screen visible.
    pygame.display.flip()
    
    # Pause
    sleep(1)