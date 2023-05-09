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
from models import Spaceship


class commsManager:
    def __init__(self,create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.players = {}
        self.localPlayer = None
        self.sprites = pygame.sprite.Group()

    def addPlayer(self, ship, bullet, **kwargs):
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
            player = Spaceship((400,300),self.create_bullet_callback, ship, bullet, id=name)
            self.players[name] = player

    def update(self,screen):
        for id, player in self.players.items():
            player.move(screen)

        for id, player in self.players.items():
            if player.destroyed:
                self.players.pop(id)
                break


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
        shoot = data.get("shoot", False)
        damage = data.get("damage", None)
        destroyed = data.get("destroyed", None)
        kills = data.get("kills", None)
        ship = data.get("ship", None)
        bullet = data.get("bullet", None)


        # if scoreTo is not None:
        #     print(scoreTo)
        #     print(self.players)

        if self.localPlayer != sender:
            #print(f"not local: {sender} != {self.localPlayer}")
            if not sender in self.players:
                self.addPlayer(ship, bullet, name=sender)
                print(f"Players: {len(self.players)}")
            else:
                if xy:
                    self.players[sender].position.x = xy[0]
                    self.players[sender].position.y = xy[1]
                if vel:
                    self.players[sender].velocity.x = vel[0]
                    self.players[sender].velocity.y = vel[1]
                if dir:
                    self.players[sender].direction.x = dir[0]
                    self.players[sender].direction.y = dir[1]
                if shoot is True:
                    self.players[sender].shoot()
                if damage:
                    self.players[sender].damage = damage
                if destroyed:
                    self.players[sender].destroyed = destroyed

                if kills:
                    self.players[sender].kills = kills

        else:
            # print("local player")
            pass