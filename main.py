import pygame
import sys
import spritesheet

from pytmx.util_pygame import load_pygame

def main():
    
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    fps = 60
    moveframes = 32
    pygame.display.set_caption("Desert Island")

    # Color library
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)

    Level1 = load_pygame('DesertIsland.tmx')
    Level1_group = pygame.sprite.Group()
    players = pygame.image.load('sprites/pngegg.png').convert_alpha()
    player_group = pygame.sprite.Group()
    #print(tmx_data.layers) # Print all layers

    direction_x = 0
    direction_y = 0

    player_1_sheet = spritesheet.SpriteSheet(players)

    # def get_player_image(player, frame, width, height, scale):
    #     player_image = pygame.Surface((width, height), pygame.SRCALPHA)
    #     player_image.blit(player, (0, 0), ((frame * width), 0, width, height))
    #     player_image = pygame.transform.scale(player_image, (width * scale, height * scale))
    #     return player_image
    
    player_animation = []
    player_animation_steps = 0
    action = 0
    player = 0
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


    # class Player(pygame.sprite.Sprite):
    #     def __init__(self, pos, image, group):
    #         super().__init__(group)
    #         self.image = image
    #         self.rect = self.image.get_rect(topleft = pos)

    # Get tiles for a specific layer - Floor
    # Sand = tmx_data.get_layer_by_name('Sand')
    # Water = tmx_data.get_layer_by_name('Water')
    # Water2 = tmx_data.get_layer_by_name('Water2')
    # Terrain = tmx_data.get_layer_by_name('Terrain')

    # screen.blit(player_1_sheet.get_player_image(player_animation_steps, action, 32, 32, 1), (400, 300))
    
    class Player():
        def __init__(self, pos, image, group)-> None:
            super().__init__(group)
            self.image = image
            self.rect = [32,32]

        def get_image(self, frame, action, width, height, scale):
            player_image = player_1_sheet
            player_image.blit(self.image, (0, 0), ((frame * width), action * height, width, height))
            player_image = pygame.transform.scale(player_image, (width * scale, height * scale))
            return player_image
        
    player1 = Player((0,0), player_1_sheet, player_group)

    running = True  # Game loop
    while running:



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    action = 1
                    player_animation_steps += 1
                    direction_x += moveframes

                elif event.key == pygame.K_RIGHT:
                    action = 2
                    player_animation_steps += 1
                    direction_x -= moveframes

                elif event.key == pygame.K_UP:
                    action = 3
                    player_animation_steps += 1
                    direction_y += moveframes

                elif event.key == pygame.K_DOWN:
                    action = 0
                    player_animation_steps += 1
                    direction_y -= moveframes
            

        screen.fill(black)    
        blit_all_layers(screen, Level1, (direction_x, direction_y), (-600,0))

        current_time = pygame.time.get_ticks()

        # if current_time - last_update >= player_animation_speed:
        #     last_update = current_time
        #     player_frame += 1
        # if player_frame == len(player_animation[player]):
        #     player_frame = 0
        # if player_frame == len(player_animation[action]):
        #     player_frame = 0

        # screen.blit(player_1_sheet.get_player_image(player_animation_steps, action, 32, 32, 1), (400, 300))

        player1.get_image(player_animation_steps, action, 32, 32, 1) 

        # if player_animation_steps == 3:
        #     player_animation_steps = 0
        Level1_group.draw(screen)
        
        pygame.display.update()
        
        clock.tick(fps)
if __name__ == "__main__":
    main()
    pygame.quit()  # Quit the game
    sys.exit()
