import pygame


class Food:

    color = "chartreuse3"

    def __init__(self, area, x, y, radius):
        self.area = area
        self.x = x
        self.y = y
        self.radius = radius
        area.elements.append(self)
  
    def tick(self):
       pass
 
    def draw(self):
       pygame.draw.circle(self.area.ant_layer, pygame.Color(self.color), (self.x, self.y), self.radius)
      