import pygame
import sys
import spritesheet
import pytmx
import random

from rich import json
from pytmx.util_pygame import load_pygame
from player import Player
from tilemap import TiledMap
from utils import get_random_position, load_sprite, print_text, load_sound, mykwargs
from manager import commsManager
from urllib.request import urlopen
from monsters import NPC

# Color library
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

time_elapse = 500

pygame.mixer.init()
pygame.mixer.music.load("sounds/song21.wav")

display_time = 1000  # Time in milliseconds to display each image

class DesertIsland:
    def __init__(self):
        """
        To Run: py/python __main__.py game-01 player-01
        """
        url = "https://terrywgriffin.com/current_usage.json"
        response = urlopen(url)
        data_json = json.loads(response.read())
        if len(data_json['players']) >= 10:
            print(data_json['players'])
            print("max users exceed!")
            exit(111)

        args, kwargs = mykwargs(sys.argv)

        queue = kwargs.get("queue", None)
        playerId = kwargs.get("player", None)
        creds = {
            "exchange": queue,
            "port": "5672",
            "host": "terrywgriffin.com",
            "user": playerId,
            "password": playerId + "2023!!!!!",
        }

        self._init_pygame()
        self.arial = pygame.font.SysFont("Arial", 18)
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.monsters = []
        self.bullets = []
        self.weapon_bag = []
        self.spritenum = random.randrange(1, 10, 1)
        self.sprite_width = 32
        self.sprite_height = 32
        
        self.manager = commsManager(self.bullets.append)
        localPlayer = Player(self.spritenum , self.bullets.append, self.sprite_width, self.sprite_height, (400, 300), id=playerId, creds=creds, callback= self.manager.callBack)
        self.manager.addPlayer(None, player=localPlayer, localPlayer=True)
        self.player = localPlayer
        self.direction_x = 0
        self.direction_y = 0
        # self.manager.addPlayer(None, None, player=localPlayer, localPlayer=True)
        # self.player = localPlayer


        if len(self.monsters) < 10:
            for i in range(10):
                # self.monsters.append(NPC((random.randrange(10, 790, 1), random.randrange(10, 790, 1)), self.bullets.append, random.choice(ships), self.targets))
                pass

    def blit_layer(self, window, tmx_data, layer_name, world_offset, start):
        layer = tmx_data.get_layer_by_name(layer_name)
        for x, y, image in layer.tiles():
            pos = (x * 32 + world_offset[0]+ start[0], y * 32 + world_offset[1]+ start[1])
            window.blit(image, pos)

    def blit_all_layers(self, window, tmx_data, world_offset, start):
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for image in layer.tiles():
                    pos = (image[0] * 32 + world_offset[0]+ start[0], image[1] * 32 + world_offset[1]+ start[1])
                    window.blit(image[2], pos)

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Desert Island")

    def main(self):

        fps = 60
        moveframes = 1
        

        Level1 = load_pygame('DesertIsland.tmx')
        weapon_sheet = pygame.image.load("sprites/weapons.png")
        # Level1_group = pygame.sprite.Group()

        # sprite_sheet_path = f'sprites/Player{spritenum}.png'

        x = 400
        y = 300

        # players = pygame.image.load(f'sprites/Player{random.randrange(1, 7, 1)}.png').convert_alpha()
        # player_group = pygame.sprite.Group()
        #print(tmx_data.layers) # Print all layers

        # Get tiles for all layers
        # maps = TiledMap('DesertIsland.tmx')

        health = self.player.health
        points = self.player.points


        # Get tiles for a specific layer - Floor
        # Sand = tmx_data.get_layer_by_name('Sand')
        # Water = tmx_data.get_layer_by_name('Water')
        Water2 = Level1.get_layer_by_name('Water2')
        # Terrain = tmx_data.get_layer_by_name('Terrain')
        # Landscape = tmx_data.get_layer_by_name('Landscape')
        # print(Water2.offsetx)

        map = TiledMap('DesertIsland.tmx')

        collisions = []
        # for layer in Level1.get_layer_by_name('Water2'):
        for x, y, gid in Water2.tiles():
            tile_properties = Level1.get_tile_properties_by_gid(gid)
            if tile_properties and tile_properties.get("collision"):
                rect = pygame.Rect(x *  Level1.tilewidth, y *  Level1.tileheight,
                                    Level1.tilewidth,  Level1.tileheight)
                collisions.append(rect)
            # print(rect)
            # pygame.draw.rect(surf, (255, 0, 0), rect)
            # pass
            #This is all wrong
            # print(Water2.properties[1])
            # collisions.append(pygame.Rect(x * Water2.tilewidth, y * Water2.tileheight,
                                #    Water2.tilewidth, Water2.tileheight))

        # blockers = []
        # tilewidth = tile_renderer.tmx_data.tilewidth
        # for tile_object in tile_renderer.tmx_data.getObjects():
        #     properties = tile_object.__dict__
        #     if properties['name'] == 'Water2':
        #         x = properties['x'] 
        #         y = properties['y']
        #         width = properties['width']
        #         height = properties['height']
        #         new_rect = pg.Rect(x, y, width, height)
        #         blockers.append(new_rect)
        
        # Add weapons to the player's bag
        weapon_icon_position = (150, 150)  # Replace with the desired position of the weapon icon
        self.player.add_weapon(weapon_sheet.subsurface(pygame.Rect(0, 0, 32, 32)), weapon_icon_position)


        all_sprites = pygame.sprite.Group()
        all_sprites.add(self.player)

        running = True  # Game loop
        while running:
            points_image = self.arial.render(f"Points: {points}", 1, (255,255,255))
            health_image = self.arial.render("Health: "+str(health), 1, (255,255,255) )


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
            # Update player position and sprite
            keys = pygame.key.get_pressed()
            self.player.update(keys, (self.direction_x, self.direction_y))

            # self.screen.fill(black)    
            # blit_all_layers(screen, Level1, (direction_x, direction_y), (-600,0))

            # map.render(screen)

            for collision_rect in collisions:
                # if player.rect.top > collision_rect.bottom:
                #     player.rect.y += 10
                print(collision_rect)
                # rectangle1 = pygame.Rect(10, 30, 50, 70)
                # pygame.draw.rect(screen, red, collision_rect)


            current_time = pygame.time.get_ticks()

            # Check for collisions with the collision layer
            # for collision_object in Water2:
            #     if collision_object.collides_with(player):
            #         print("Collision")
            #         # Handle collision, e.g. prevent the player from moving through the object
            #         if player.rect.left < collision_object.rect.right and player.rect.right > collision_object.rect.right:
            #             player.rect.right = collision_object.rect.left
            #         if player.rect.right > collision_object.rect.left and player.rect.left < collision_object.rect.left:
            #             player.rect.left = collision_object.rect.right
            #         if player.rect.top < collision_object.rect.bottom and player.rect.bottom > collision_object.rect.bottom:
            #             player.rect.bottom = collision_object.rect.top
            #         if player.rect.bottom > collision_object.rect.top and player.rect.top < collision_object.rect.top:
            #             player.rect.top = collision_object.rect.bottom

            # for x, y, data in Water2.tiles():
            #     print(data)
                # pos = (x * 32, y * 32)
                # if player.rect.right > pos[0]:
                #     player.rect.left =pos[0]

                # if player.rect.bottom > pos[1]:
                #     player.rect.top =pos[1]

            for bullet in self.bullets[:]:
                if bullet.collides_with(self.player) and bullet.id != self.player.id:
                    self.player.hit()
                    self.player.sendData()
                    self.bullets.remove(bullet)
                    break

            # Keep player within screen limits
            if self.player.rect.y < 150: 
                self.player.rect.y = 150
                self.direction_y += moveframes
            if self.player.rect.y > 450: 
                self.player.rect.y = 450
                self.direction_y -= moveframes
            if self.player.rect.x < 150: 
                self.player.rect.x = 150
                self.direction_x += moveframes
            if self.player.rect.x > self.screen.get_width()-150: 
                self.player.rect.x = self.screen.get_width()-150
                self.direction_x -= moveframes

            self.blit_layer(self.screen, Level1, 'Water', (self.direction_x, self.direction_y), (-600,0))
            self.blit_layer(self.screen, Level1, 'Water2', (self.direction_x, self.direction_y), (-600,0))
            self.blit_layer(self.screen, Level1, 'Sand', (self.direction_x, self.direction_y), (-600,0))
            self.blit_layer(self.screen, Level1, 'Terrain', (self.direction_x, self.direction_y), (-600,0))
            self.blit_layer(self.screen, Level1, 'Landscape', (self.direction_x, self.direction_y), (-600,0))
            

            # Level1_group.draw(screen)

            all_sprites.draw(self.screen)
            self.manager.draw(self.screen)

            for bullet in self.bullets:
                bullet.move(self.screen)
                bullet.draw(self.screen)


                # Draw the weapons in the bag if it's open
            if self.player.bag_open:
                for weapon in self.player.weapon_bag:
                    self.screen.blit(weapon.image, weapon.rect.topleft)

            # for collision_rect in collisions:
            #     if player.rect.colliderect(collision_rect):
            #         print("collision")

            self.screen.blit(points_image, (50, 10))
            self.screen.blit(health_image, (50, 30))
            
            pygame.display.update()
            
            self.clock.tick(fps)