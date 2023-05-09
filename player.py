import pygame
from messenger import Messenger

# necessary libs for rabbitmq
from comms import CommsListener
from comms import CommsSender

class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, sprite_width, sprite_height, x, y, **kwargs):
        
        
        # Load the sprite sheet image and set up the player's initial sprite
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.current_sprite_x = 0
        self.current_sprite_y = 0
        self.image = self.get_sprite(self.current_sprite_x, self.current_sprite_y)
        
        # Set up the player's rect and initial position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100
        self.points = 0
        
        # Set up animation variables
        self.animation_timer = 0
        self.animation_delay = 1
        
        # Set up movement variables
        self.speed = 1

        self.creds = kwargs.get("creds", None)
        self.callback = kwargs.get("callback", None)
        self.id = kwargs.get("id", None)

        if self.creds is not None:
            self.messenger = Messenger(self.creds, self.callback)
        self.lastBroadcast = pygame.time.get_ticks()
        self.broadCastDelay = 0

        super().__init__()

    def timeToBroadCast(self):
        """check to see if there was enough delay to broadcast again"""
        return pygame.time.get_ticks() - self.lastBroadcast > self.broadCastDelay

    def broadcastData(self, data):
        if self.timeToBroadCast():
            self.messenger.send(
                target="broadcast", sender=self.id, player=self.id, data=data
            )
            self.lastBroadcast = pygame.time.get_ticks()
            return True

        return False

    def get_sprite(self, x, y):
        """Get a single sprite image from the sprite sheet."""
        sprite = pygame.Surface((32, 32), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), (x * 32, y * 32, 32, 32))
        return sprite
    
    def animate(self):
        """Update the player's sprite animation."""
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            self.current_sprite_x = (self.current_sprite_x + 1) % 3
            self.image = self.get_sprite(self.current_sprite_x, self.current_sprite_y)
    
    def update(self, keys):
        """Update the player's position based on user input."""
        if keys[pygame.K_LEFT]:
            self.current_sprite_y = 1
            self.rect.x -= self.speed
            self.animate()
        if keys[pygame.K_RIGHT]:
            self.current_sprite_y = 2
            self.rect.x += self.speed
            self.animate()
        if keys[pygame.K_UP]:
            self.current_sprite_y = 3
            self.rect.y -= self.speed
            self.animate()
        if keys[pygame.K_DOWN]:
            self.current_sprite_y = 0
            self.rect.y += self.speed
            self.animate()
    
    def draw(self, surface):
        """Draw the player's sprite to a Pygame surface."""
        surface.blit(self.image, self.rect)

    def sendData(self):
        self.broadcastData(
            {
                "pos": (self.position.x, self.position.y),
                "vel": (self.velocity[0], self.velocity[1]),
                "dir": (self.direction.x, self.direction.y),
                "shoot": False,
                "damage": self.damage,
                "destroyed": self.destroyed,
                "ship":self.ship,
                "bullet":self.bullet,
                "kills":self.kills
            }
        )

    def sendShoot(self):
        self.broadcastData(
            {
                "pos": (self.position.x, self.position.y),
                "vel": (self.velocity[0], self.velocity[1]),
                "dir": (self.direction.x, self.direction.y),
                "shoot": True,
                "damage": self.damage,
                "destroyed": self.destroyed
            }
        )
