import pygame

class Area:

    def __init__(self, width, height, caption, spray_decrease_ticks):
        self.elements = []
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        self.ant_layer = pygame.Surface((width, height))
        self.pheromone_layer = pygame.Surface((width, height))
        self.decrease_layer = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.decrease_layer, (0, 0, 0, 1), (0, 0, width, height))
        pygame.display.set_caption(caption)
        self.spray_decrease_ticks = spray_decrease_ticks
        self.spray_decrease_current_ticks = 0

    def tick(self):
        for element in self.elements:
            element.tick()
        self.decrease_spray()
        self.draw()
    
    def draw(self):
        self.window.fill(("black"))
        self.ant_layer.fill(("black"))
        for element in self.elements:
            element.draw()
        self.window.blit(self.pheromone_layer, (0, 0), special_flags = pygame.BLEND_RGBA_ADD)
        self.window.blit(self.ant_layer, (0, 0), special_flags = pygame.BLEND_RGBA_ADD)
        pygame.display.update()

    def spray(self, x, y, mode, spray_intensity):
        if mode == "search":
            color = self.pheromone_layer.get_at((x, y))
            old_value = color.b
            new_value = old_value + spray_intensity
            if new_value > 255:
                new_value = 255
            color.b = new_value
            self.pheromone_layer.set_at((x, y), color)
        if mode == "return":
            color = self.pheromone_layer.get_at((x, y))
            old_value = color.r
            new_value = old_value + spray_intensity
            if new_value > 255:
                new_value = 255
            color.r = new_value
            self.pheromone_layer.set_at((x, y), color)

    def decrease_spray(self):
        self.spray_decrease_current_ticks += 1
        if self.spray_decrease_current_ticks >= self.spray_decrease_ticks:
            self.pheromone_layer.blit(self.decrease_layer, (0, 0))
            self.spray_decrease_current_ticks = 0