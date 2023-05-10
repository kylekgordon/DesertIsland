from pygame.math import Vector2
from pygame import transform
import json
import time
import sys
import pygame
import random
from utils import get_random_velocity, load_sound, load_sprite, wrap_position, distance
import math
import os

from gameobject import GameObject
from rich import print
from threading import Thread
# necessary libs for rabbitmq
from comms import CommsListener
from comms import CommsSender

UP = Vector2(0, -1)

# Color library
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

bullet = 37

class NPC(GameObject):
    def __init__(
        self, position, create_bullet_callback, sprite_sheet_path, attack = f"sprites/Bullets/{bullet}.png" , targets=[]
    ):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.current_sprite_x = 0
        self.current_sprite_y = 0
        self.image = self.get_sprite(self.current_sprite_x, self.current_sprite_y)
        
        # Set up the player's rect and initial position
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.health = 100
        self.points = 0
        
        # Set up animation variables
        self.animation_timer = 0
        self.animation_delay = 1

        self.targets = targets
        self.damage = 0
        self.speed = 0.00001
        self.countShootTime = 0

        super().__init__(position, create_bullet_callback, sprite_sheet_path, attack)

    def choose_target(self):
        closestDistance = pow(2, 20)
        closestTarget = None
        for target in self.targets:
            d = distance(target.position, self.position)
            if distance(target.position, self.position) < closestDistance:
                closestTarget = target
                closestDistance = d

        self.target = closestTarget

    def follow_target(self):
        if self.target:
            self.direction = Vector2(self.target.position.x - self.position.x, self.target.position.y - self.position.y)
            self.direction = self.direction.normalize()
            self.velocity = Vector2(self.direction.x, self.direction.y)

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

    # def shoot(self):
    #     self.countShootTime += 0.016
    #     if self.countShootTime >= 3 and self.target:
    #         self.countShootTime = 0
    #         angle = self.direction.angle_to(UP)
    #         bullet_velocity = self.direction * self.BULLET_SPEED/2 + self.velocity
    #         bullet = Bullet(self.position, bullet_velocity, None, angle, "npc")
    #         self.create_bullet_callback(bullet)
    #         self.laser_sound.play()

    def damage_bar(self, screen):
        pygame.draw.rect(screen, (red), (self.position.x - 25, self.position.y - 60, 50, 5))
        pygame.draw.rect(screen, (green), (self.position.x - 25, self.position.y - 60, 50 - (self.damage/2), 5))
        #screen.blit(current_image, (self.position.x - 50, self.position.y - 60))

    def remove(self):
        pass