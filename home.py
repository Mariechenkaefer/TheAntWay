import random
import pygame

from ant import Ant


class Home:
   
    color = "antiquewhite4"

    def __init__(self, area, food, x, y, radius, 
                 ant_count, ant_max_spray_intensity, ant_max_duration_to_spray, ant_steps_to_spray, ant_steps_to_ignore, 
                 sample_count, sample_min_length, sample_max_length, ant_spray_decrease,
                 ant_surrounding_angle, ant_angle, ant_color_search, ant_color_return):
        self.area = area
        self.food = food
        self.x = x
        self.y = y
        self.radius = radius
        self.ants = []
        self.ant_count = ant_count
        self.ant_max_spray_intensity = ant_max_spray_intensity
        self.ant_max_duration_to_spray = ant_max_duration_to_spray
        self.ant_steps_to_spray = ant_steps_to_spray
        self.ant_steps_to_ignore = ant_steps_to_ignore
        self.sample_count = sample_count
        self.sample_min_length = sample_min_length
        self.sample_max_length = sample_max_length
        self.ant_spray_decrease = ant_spray_decrease
        self.ant_surrounding_angle = ant_surrounding_angle
        self.ant_angle = ant_angle
        self.ant_color_search = ant_color_search
        self.ant_color_return = ant_color_return
        area.elements.append(self)
  
    def tick(self):
        self.spawn_ants()

    def spawn_ants(self):
        if len(self.ants) < self.ant_count:
            debug_ant = False # (len(self.ants)==50)
            my_ant = Ant(
                area = self.area,
                home = self,
                food = self.food,
                x = self.x,
                y = self.y,
                color_search = self.ant_color_search,
                color_return = self.ant_color_return,
                max_duration_to_spray = self.ant_max_duration_to_spray,
                max_spray_intensity = self.ant_max_spray_intensity,
                steps_to_spray = self.ant_steps_to_spray,
                steps_to_ignore = self.ant_steps_to_ignore,
                sample_count = self.sample_count, 
                sample_min_length = self.sample_min_length, 
                sample_max_length = self.sample_max_length, 
                ant_spray_decrease = self.ant_spray_decrease,
                surrounding_angle = self.ant_surrounding_angle,
                angle = self.ant_angle,
                is_debug = debug_ant,
                color_debug = "green")
            self.ants.append(my_ant)

 
    def draw(self):
       pygame.draw.circle(self.area.ant_layer, pygame.Color(self.color), (self.x, self.y), self.radius)
       