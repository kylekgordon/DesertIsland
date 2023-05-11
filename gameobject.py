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

from rich import print
from threading import Thread
# necessary libs for rabbitmq
from comms import CommsListener
from comms import CommsSender

UP = Vector2(0, -1)

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = 32 / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)
        # print(f"pos: {self.position}")

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

    def collides_withPos(self, other_obj,pos):
        distance = self.position.distance_to(pos)
        return distance < self.radius + other_obj.radius