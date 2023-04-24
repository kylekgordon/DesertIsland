import pygame
import sys
import spritesheet

from pytmx.util_pygame import load_pygame
from player import Player
from tilemap import TiledMap

def main():
    
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    fps = 60
    moveframes = 64
    pygame.display.set_caption("Desert Island")

    # Color library
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)

    Level1 = load_pygame('DesertIsland.tmx')
    Level1_group = pygame.sprite.Group()


    sprite_sheet_path = "sprites/Player3.png"
    sprite_width = 32
    sprite_height = 32
    x = 400
    y = 100

    player = Player(sprite_sheet_path, sprite_width, sprite_height, x, y)

    players = pygame.image.load('sprites/Player1.png').convert_alpha()
    player_group = pygame.sprite.Group()
    #print(tmx_data.layers) # Print all layers

    direction_x = 0
    direction_y = 0

    player_1_sheet = spritesheet.SpriteSheet(players)
    
    player_animation = []
    player_animation_steps = 0
    action = 0
    # player = 0
    last_update = pygame.time.get_ticks()
    player_animation_speed = 75
    player_frame = 0
    step_counter = 0

    # for x in range(3):
    #     temp_list = []
    #     for y in range(4):
    #         player_animation.append(sprite_sheet.get_player_image(x*32, y*32, 32, 32, 1))

    # print(player_animation)
    # for animation in player_animation_steps:
    #     temp_list = []
    #     for _ in range(animation):
    #         temp_list.append(sprite_sheet.get_player_image(step_counter, action, 32, 32, 1))
    #         step_counter += 1
    #     player_animation.append(temp_list)
    # #frame_0 = sprite_sheet.get_player_image(2, 32, 32, 1)

    def blit_all_layers(window, tmx_data, world_offset, start):
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for image in layer.tiles():
                    pos = (image[0] * 32 + world_offset[0]+ start[0], image[1] * 32 + world_offset[1]+ start[1])
                    window.blit(image[2], pos)

    # Get tiles for all layers
    # class Tile(pygame.sprite.Sprite):
    #     def __init__(self, pos, image, group):
    #         super().__init__(group)
    #         self.image = image
    #         self.rect = self.image.get_rect(topleft = pos)

    #     def update(self, window, offset):
    #         window.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))

    # for layer in Level1.visible_layers: # all visible layers
    #     if hasattr(layer, 'data'):
    #         for x, y, image in layer.tiles():
    #             pos = (x * 32, y * 32)
    #             Tile(pos = pos, image = image, group = Level1_group)

    # Get tiles for a specific layer - Floor
    # Sand = tmx_data.get_layer_by_name('Sand')
    # Water = tmx_data.get_layer_by_name('Water')
    Water2 = Level1.get_layer_by_name('Water2')
    # Terrain = tmx_data.get_layer_by_name('Terrain')
    # Landscape = tmx_data.get_layer_by_name('Landscape')

    def blit_layer(window, tmx_data, layer_name, world_offset, start):
        layer = tmx_data.get_layer_by_name(layer_name)
        for x, y, image in layer.tiles():
            pos = (x * 32 + world_offset[0]+ start[0], y * 32 + world_offset[1]+ start[1])
            window.blit(image, pos)
        
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True  # Game loop
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    # action = 1
                    # player_animation_steps += 1
                    direction_x += moveframes

                elif event.key == pygame.K_RIGHT:
                    # action = 2
                    # player_animation_steps += 1
                    direction_x -= moveframes

                elif event.key == pygame.K_UP:
                    # action = 3
                    # player_animation_steps += 1
                    direction_y += moveframes

                elif event.key == pygame.K_DOWN:
                    # action = 0
                    # player_animation_steps += 1
                    direction_y -= moveframes
                
        # Update player position and sprite
        keys = pygame.key.get_pressed()
        player.update(keys)

        screen.fill(black)    
        blit_all_layers(screen, Level1, (direction_x, direction_y), (-600,0))

        current_time = pygame.time.get_ticks()


        # Check for collisions with the collision layer
        # for collision_object in Water2:
        #     if player.rect.colliderect(collision_object):
        #         # Handle collision, e.g. prevent the player from moving through the object
        #         if player.rect.left < collision_object.rect.right and player.rect.right > collision_object.rect.right:
        #             player.rect.right = collision_object.rect.left
        #         if player.rect.right > collision_object.rect.left and player.rect.left < collision_object.rect.left:
        #             player.rect.left = collision_object.rect.right
        #         if player.rect.top < collision_object.rect.bottom and player.rect.bottom > collision_object.rect.bottom:
        #             player.rect.bottom = collision_object.rect.top
        #         if player.rect.bottom > collision_object.rect.top and player.rect.top < collision_object.rect.top:
        #             player.rect.top = collision_object.rect.bottom

        # screen.blit(player_1_sheet.get_player_image(player_animation_steps, action, 32, 32, 1), (400, 300))
        # if player_animation_steps == 3:
        #     player_animation_steps = 0

        Level1_group.draw(screen)

        all_sprites.draw(screen)

        # blit_layer(screen, Level1, 'Landscape', (player.rect.x, player.rect.y), (-600,0))
        
        pygame.display.update()
        
        clock.tick(fps)
if __name__ == "__main__":
    main()
    pygame.quit()  # Quit the game
    sys.exit()
