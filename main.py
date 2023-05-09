import pygame
import sys
import spritesheet
import pytmx
import random

from pytmx.util_pygame import load_pygame
from player import Player
from tilemap import TiledMap

def blit_layer(window, tmx_data, layer_name, world_offset, start):
    layer = tmx_data.get_layer_by_name(layer_name)
    for x, y, image in layer.tiles():
        pos = (x * 32 + world_offset[0]+ start[0], y * 32 + world_offset[1]+ start[1])
        window.blit(image, pos)

def blit_all_layers(window, tmx_data, world_offset, start):
    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'data'):
            for image in layer.tiles():
                pos = (image[0] * 32 + world_offset[0]+ start[0], image[1] * 32 + world_offset[1]+ start[1])
                window.blit(image[2], pos)

def main():
    
    pygame.init()
    arial = pygame.font.SysFont("Arial", 18)
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    fps = 60
    moveframes = 1
    pygame.display.set_caption("Desert Island")

    # Color library
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)

    Level1 = load_pygame('DesertIsland.tmx')
    # Level1_group = pygame.sprite.Group()

    sprite_sheet_path = f'sprites/Player{random.randrange(1, 10, 1)}.png'
    sprite_width = 32
    sprite_height = 32
    x = 400
    y = 300

    player = Player(sprite_sheet_path, sprite_width, sprite_height, x, y)

    players = pygame.image.load(f'sprites/Player{random.randrange(1, 7, 1)}.png').convert_alpha()
    # player_group = pygame.sprite.Group()
    #print(tmx_data.layers) # Print all layers

    # Get tiles for all layers
    # maps = TiledMap('DesertIsland.tmx')

    health = player.health
    points = player.points

    direction_x = 0
    direction_y = 0

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
        
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True  # Game loop
    while running:
        points_image = arial.render(f"Points: {points}", 1, (255,255,255))
        health_image = arial.render("Health: "+str(health), 1, (255,255,255) )


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
             
        # Update player position and sprite
        keys = pygame.key.get_pressed()
        player.update(keys)

        screen.fill(black)    
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


        # Keep player within screen limits
        if player.rect.y < 150: 
            player.rect.y = 150
            direction_y += moveframes
        if player.rect.y > 450: 
            player.rect.y = 450
            direction_y -= moveframes
        if player.rect.x < 150: 
            player.rect.x = 150
            direction_x += moveframes
        if player.rect.x > screen.get_width()-150: 
            player.rect.x = screen.get_width()-150
            direction_x -= moveframes

        blit_layer(screen, Level1, 'Water', (direction_x, direction_y), (-600,0))
        blit_layer(screen, Level1, 'Water2', (direction_x, direction_y), (-600,0))
        blit_layer(screen, Level1, 'Sand', (direction_x, direction_y), (-600,0))
        blit_layer(screen, Level1, 'Terrain', (direction_x, direction_y), (-600,0))
        blit_layer(screen, Level1, 'Landscape', (direction_x, direction_y), (-600,0))
        

        # Level1_group.draw(screen)

        all_sprites.draw(screen)


        # for collision_rect in collisions:
        #     if player.rect.colliderect(collision_rect):
        #         print("collision")

        screen.blit(points_image, (50, 10))
        screen.blit(health_image, (50, 30))
        
        pygame.display.update()
        
        clock.tick(fps)


if __name__ == "__main__":
    main()
    pygame.quit()  # Quit the game
    sys.exit()
