import pygame

class SpriteSheet():
    def __init__(self, image) -> None:
        self.player = image

    def get_player_image(self, frame, action, width, height, scale):
        player_image = pygame.Surface((width, height), pygame.SRCALPHA)
        player_image.blit(self. player, (0, 0), ((frame * width), (action * height), width, height))
        player_image = pygame.transform.scale(player_image, (width * scale, height * scale))
        return player_image