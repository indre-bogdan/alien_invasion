class Settings():
    """A class to store the settings for the game"""
    
    def __init__(self):
        """Initialize the game`s static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        
        # Ship settings
        self.ship_limit  = 3
        
        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        
        # Alien settings
        self.fleet_drop_speed = 5
        
        # How quickly the game speeds up 
        self.speedup_scale = 1.1
        
        # How quickly the alien point value increase
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        
        # A fleet direction = 1 means right, -1 means left
        self.fleet_direction = 1
        
        # Scoring
        self.alien_points = 2
    
    def increase_speed(self):
        """Increases speed settings and alien points value."""
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        