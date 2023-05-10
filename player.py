import pygame
import math
import os
import random

from messenger import Messenger
from pygame.math import Vector2
from pygame import transform
from utils import get_random_velocity, load_sound, load_sprite, wrap_position, distance
from gameobject import GameObject
# necessary libs for rabbitmq
from threading import Thread
from comms import CommsListener
from comms import CommsSender

DOWN = Vector2(0, 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, playernum, create_bullet_callback, sprite_width, sprite_height, position, **kwargs):
        
        self.create_bullet_callback = create_bullet_callback
        # Load the sprite sheet image and set up the player's initial sprite
        self.sprite_sheet = pygame.image.load(f'sprites/Player{playernum}.png').convert_alpha()
        self.current_sprite_x = 0
        self.current_sprite_y = 0
        self.image = self.get_sprite(self.current_sprite_x, self.current_sprite_y)
        
        # Set up the player's rect and initial position
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.health = 100
        self.points = 0
        self.playernum = playernum
        self.bulletnum = 0
        self.direc = Vector2(1,0)
        
        # Set up animation variables
        self.animation_timer = 0
        self.animation_delay = 1
        self.direction = ""
        # Set up movement variables
        self.speed = 1
        self.velocity = (0, 0)

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
            self.direc = Vector2(-1,0)
            self.rect.x -= self.speed
            self.sendData()
            self.animate()
        if keys[pygame.K_RIGHT]:
            self.current_sprite_y = 2
            self.direc = Vector2(1,0)
            self.rect.x += self.speed
            self.sendData()
            self.animate()
        if keys[pygame.K_UP]:
            self.current_sprite_y = 3
            self.direc = Vector2(0,-1)
            self.rect.y -= self.speed
            self.sendData()
            self.animate()
        if keys[pygame.K_DOWN]:
            self.current_sprite_y = 0
            self.direc = Vector2(0,1)
            self.rect.y += self.speed
            self.sendData()
            self.animate()
        if keys[pygame.K_SPACE]:
            self.attack()
            self.sendAttack()
    
    def draw(self, surface):
        """Draw the player's sprite to a Pygame surface."""
        surface.blit(self.image, self.rect)

    def sendData(self):
        self.broadcastData(
            {
                "pos": (self.rect.x, self.rect.y),
                "sprite": (self.current_sprite_y),
                "vel": (self.velocity[0], self.velocity[1]),
                "dir": (self.direction, self.direction),
                "attack": False,
                "health": self.health,
                "player":self.playernum,
                "points":self.points,
                "direction": self.direction
            }
        )

    def sendAttack(self):
        self.broadcastData(
            {
                "pos": (self.rect.x, self.rect.y),
                "vel": (self.velocity[0], self.velocity[1]),
                "dir": (self.direction, self.direction),
                "attack": True,
                "damage": self.health,
                "direction": self.direction
            }
        )

    def attack(self):
        angle = 0  # update this as needed
        bullet_velocity = self.direc * 10  # Bullet speed is 10 units/frame
        bullet = Bullet((self.rect.x, self.rect.y), bullet_velocity, self.id, angle, "player")
        self.create_bullet_callback(bullet)


bullet = random.randrange(10, 66, 1)

class Bullet(GameObject):
    def __init__(self, position, velocity, id, angle, belongTo):
        
        super().__init__(position, load_sprite(f"/Bullets/{bullet}"), velocity)
        #self.sprite = pygame.transform.scale(self.sprite, (30, 30))
        #adjust the angle for the sprite
        angle2 = math.degrees(math.atan2(-velocity.y, velocity.x)) + 90
        self.sprite = pygame.transform.rotozoom(self.sprite, angle2, 0.3)
        if self.sprite.get_size() == (0, 0):
            print(f"Error: sprite 'Bullets/{bullet}.png' is empty or not valid")
        self.radius = self.sprite.get_width() / 2
        self.id = id
        self.belongTo = belongTo
        
    def move(self, surface):
        self.position = self.position + self.velocity

    def draw(self, surface):
    # """Draw the bullet's sprite to a Pygame surface."""
        surface.blit(self.sprite, tuple(self.position))

        