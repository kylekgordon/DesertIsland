import pygame
import pytmx

class TiledMap:
    def __init__(self, tmx_file):
        self.tmx_data = pytmx.util_pygame.load_pygame(tmx_file)

        # Create a dictionary of tilesets for easy reference
        self.tilesets = {}
        for tileset in self.tmx_data.tilesets:
            self.tilesets[tileset.name] = tileset
        
        # Create a list of tile layers for rendering
        self.layers = []
        for layer in self.tmx_data.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self.layers.append(layer)
        
        # Create a list of collision rects
        self.collisions = []
        for layer in self.tmx_data.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_properties = self.tmx_data.get_tile_properties_by_gid(gid)
                    if tile_properties and tile_properties.get("collision"):
                        rect = pygame.Rect(x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight,
                                           self.tmx_data.tilewidth, self.tmx_data.tileheight)
                        self.collisions.append(rect)
    
    def render(self, surface):
        """Render the Tiled map to a Pygame surface."""
        for layer in self.layers:
            for x, y, gid in layer:
                tileset = self.tmx_data.get_tileset_by_gid(gid)
                if tileset:
                    image = tileset.get_tile_image_by_gid(gid)
                    if image:
                        surface.blit(image, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

    def render_layers(self, surface, layers):
        """Render specific layers of the Tiled map to a Pygame surface."""
        for layer in self.layers:
            if layer.name in layers:
                for x, y, gid in layer:
                    tileset = self.tmx_data.get_tileset_by_gid(gid)
                    if tileset:
                        image = tileset.get_tile_image_by_gid(gid)
                        if image:
                            surface.blit(image, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))
    
    def collides_with(self, rect):
        """Check if a rectangle collides with any of the collision rects in the map."""
        for collision_rect in self.collisions:
            if rect.colliderect(collision_rect):
                return True
        return False
