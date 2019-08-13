import pygame
class Sounds():
    """A class to hold the sounds used"""
    
    def __init__(self):
        """Initialize the sounds"""
        pygame.mixer.init()
        self.shooting_sound = pygame.mixer.Sound('sounds/laser4.wav')
        self.explosion_sound = pygame.mixer.Sound('sounds/8bit_bomb_explosion.wav')
        self.next_level_sound = pygame.mixer.Sound('sounds/next_level.wav')
        
    def play_shooting_sound(self):
        pygame.mixer.Sound.play(self.shooting_sound)
        pygame.mixer.music.stop()
        
    def play_explosion_sound(self):
        pygame.mixer.Sound.play(self.explosion_sound)
        pygame.mixer.music.stop()
    def play_next_level_sound(self):
        pygame.mixer.Sound.play(self.next_level_sound)
        pygame.mixer.music.stop()