import pygame
import sys

from pytmx.util_pygame import load_pygame

def main():
    class Tile(pygame.sprite.Sprite):
        def __init__(self, pos, image, group):
            super().__init__(group)
            self.image = image
            self.rect = self.image.get_rect(topleft = pos)

        def update(self, window, offset):
            window.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))

    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    fps = 60

    pygame.display.set_caption("Desert Island")

    # Color library
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)

    Level1 = load_pygame('DesertIsland.tmx')
    Level1_group = pygame.sprite.Group()
    #print(tmx_data.layers) # Print all layers

    direction_x = 0
    direction_y = 0

    def blit_all_layers(window, tmx_data, world_offset):
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for image in layer.tiles():
                    pos = (image[0] * 32 + world_offset[0], image[1] * 32 + world_offset[1])
                    window.blit(image[2], pos)

    for layer in Level1.visible_layers: # all visible layers
        if hasattr(layer, 'data'):
            for x, y, image in layer.tiles():
                pos = (x * 32, y * 32)
                Tile(pos = pos, image = image, group = Level1_group)


    # Get tiles for a specific layer - Floor
    # Sand = tmx_data.get_layer_by_name('Sand')
    # Water = tmx_data.get_layer_by_name('Water')
    # Water2 = tmx_data.get_layer_by_name('Water2')
    # Terrain = tmx_data.get_layer_by_name('Terrain')

    running = True  # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    direction_x += 32
                    # Level1_group.update(screen, (-32, 0))
                elif event.key == pygame.K_RIGHT:
                    direction_x -= 32
                    # Level1_group.update(screen, (32, 0))
                elif event.key == pygame.K_UP:
                    direction_y += 32
                    # Level1_group.update(screen, (0, -32))
                elif event.key == pygame.K_DOWN:
                    direction_y -= 32
                    # Level1_group.update(screen, (0, 32))
            

        screen.fill(black)    
        blit_all_layers(screen, Level1, (direction_x, direction_y))

        # Level1_group.draw(screen)
        pygame.display.update()
        
        clock.tick(fps)
if __name__ == "__main__":
    main()
    pygame.quit()  # Quit the game
    sys.exit()
