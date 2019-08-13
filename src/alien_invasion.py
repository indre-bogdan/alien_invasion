import pygame
from pygame.sprite import Group
from src.settings import Settings
from src.ship import Ship
from src.game_stats import GameStats
from src.button import Button
from src.scoreboard import Scoreboard
from src.sounds import Sounds
import src.game_functions as gf

def run_game():
    """Initialize game, settings and create a screen object"""
    pygame.init()
    sounds = Sounds()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Make the play button.
    play_button = Button(ai_settings, screen, 'Play')
    
    # Make a ship, a group of aliens and a group of bullets
    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()
    
    # Create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    # Create an instance to store the game statistics and scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, sounds, aliens, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, sounds, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
            gf.update_screen(ai_settings, screen, sb, ship, aliens, bullets)
        else:
            gf.display_menu_screen(ai_settings, screen, play_button)
    
run_game()
    