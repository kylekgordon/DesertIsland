import pygame
from random import randint
import json
import sys
from rich import print
from threading import Thread
import math
import os
from pygame.math import Vector2

import pygame.display

# necessary libs for rabbitmq
from comms import CommsListener
from comms import CommsSender
from player import Player


class commsManager:
    def __init__(self,create_bullet_callback = None):
        self.create_bullet_callback = create_bullet_callback
        self.players = {}
        self.localPlayer = None
        self.sprites = pygame.sprite.Group()

    def addPlayer(self, playernum, **kwargs):
        """Adds a player to the local game as dictated by incoming messages."""
        name = kwargs.get("name", None)
        player = kwargs.get("player", None)
        localPlayer = kwargs.get("localPlayer", False)

        # Instances of players are created in two ways:
        if localPlayer:
            self.localPlayer = player.id
            self.spaceShip = player
        else:
            # This is a mirror of another player somewhere else.
            player = Player(playernum , 32, 32, (400, 300), id=name)
            self.players[name] = player

    def update(self,screen):
        for id, player in self.players.items():
            player.move(screen)

        for id, player in self.players.items():
            # if player.destroyed:
            #     self.players.pop(id)
            #     break
            pass


    def draw(self,screen):
        try:
            for id, player in self.players.items():
                player.draw(screen)
        except:
            pass

    def callBack(self, ch, method, properties, body):
        game = method.exchange  # not used here but passed in by pika
        exchange = method.exchange  # not used here but passed in by pika
        body = json.loads(body.decode("utf-8"))  # where all the game commands are
        data = body.get("data", None)
        sender = body["sender"]
        xy = data.get("pos", None)
        vel = data.get("vel", None)
        dir = data.get("dir", None)
        attack = data.get("attack", False)
        health = data.get("health", None)
        points = data.get("points", None)
        playernum = data.get("player", None)
        sprite = data.get("sprite", None)


        # if scoreTo is not None:
        #     print(scoreTo)
        #     print(self.players)

        if self.localPlayer != sender:
            #print(f"not local: {sender} != {self.localPlayer}")
            if not sender in self.players:
                self.addPlayer(playernum, name=sender)
                print(f"Players: {len(self.players)}")
            else:
                if xy:
                    self.players[sender].rect.x = xy[0]
                    self.players[sender].rect.y = xy[1]

                if sprite:
                    self.players[sender].current_sprite_y = sprite
                    self.players[sender].animate()
                else:
                    self.players[sender].current_sprite_y = 0
                    self.players[sender].animate()
                # if vel:
                #     self.players[sender].velocity[0] = vel[0]
                #     self.players[sender].velocity[1] = vel[1]
                if dir:
                    self.players[sender].direction = dir[0]
                    self.players[sender].direction = dir[1]
                if attack is True:
                    self.players[sender].attack()
                if health:
                    self.players[sender].health = health
                if points:
                    self.players[sender].points = points

        else:
            # print("local player")
            pass