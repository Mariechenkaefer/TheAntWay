from math import atan2, cos, degrees, pi, sin, radians, sqrt
import random
import pygame

class Ant: 
    current_steps = 0
    current_steps_ignored = 0

    def __init__(self, area, home, food, 
                 x, y, color_search, color_return, 
                 max_duration_to_spray, max_spray_intensity, steps_to_spray, steps_to_ignore, 
                 sample_count, sample_min_length, sample_max_length, ant_spray_decrease,
                 surrounding_angle, angle, 
                 is_debug, color_debug):
        self.area = area
        self.home = home
        self.food = food
        self.x = x
        self.y = y
        self.direction = random.randint(0, 359)
        self.angle = angle
        self.color_search = color_search
        self.color_return = color_return
        self.color_debug = color_debug
        self.max_duration_to_spray = max_duration_to_spray
        self.duration_to_spray = max_duration_to_spray
        self.max_spray_intensity = max_spray_intensity
        self.steps_to_spray = steps_to_spray
        self.steps_to_ignore = steps_to_ignore
        self.sample_count = sample_count
        self.sample_min_length = sample_min_length
        self.sample_max_length = sample_max_length
        self.ant_spray_decrease = ant_spray_decrease
        self.surrounding_angle = surrounding_angle
        self.mode = "search"
        self.is_debug = is_debug
        area.elements.append(self)

    def tick(self):
        self.debug()
        self.walk()
        self.spray()
    
    def debug(self):
        #if self.is_debug:
        #    print(self.mode, self.x, self.y, self.duration_to_spray)
        pass

    def walk(self):
        if self.mode == "search" and self.distance(self.x, self.y, self.food.x, self.food.y) < self.food.radius:
            self.mode = "return"
            self.duration_to_spray = self.max_duration_to_spray
            self.bounce_direction()
            self.walk_step()                    
        elif self.mode == "return" and self.distance(self.x, self.y, self.home.x, self.home.y) < self.home.radius:
            self.mode = "search"
            self.duration_to_spray = self.max_duration_to_spray
            self.bounce_direction()
            self.walk_step()
        else: 
            surrounding = self.get_surrounding()
            if len(surrounding) > 0:
                self.current_steps_ignored += 1
                if self.current_steps_ignored > self.steps_to_ignore:
                    target = max(surrounding, key=surrounding.get)
                    self.direction = degrees(atan2(target[1] - self.y, target[0] - self.x))                   
                    self.current_steps_ignored = 0
                    self.walk_step()
                else: 
                    self.walk_step()
            else:
                self.walk_random()

    def distance(self, x1, y1, x2, y2):
        return sqrt((y2 - y1)**2 + (x2 - x1)**2)

    def get_surrounding(self):
        surrounding = {}
        for sample in range(self.sample_count):
            sample_direction = self.direction + random.randint(-self.surrounding_angle, self.surrounding_angle)
            sample_length = random.randint(self.sample_min_length, self.sample_max_length)
            sample_cell_x = int(self.x + cos(radians(sample_direction)) * sample_length)
            sample_cell_y = int(self.y + sin(radians(sample_direction)) * sample_length)
            sample_cell = (sample_cell_x, sample_cell_y)
            if sample_cell_x < 0 or sample_cell_x > (self.area.width - 1):
                continue
            if sample_cell_y < 0 or sample_cell_y > (self.area.height - 1):
                continue
            value = 0
            if self.mode == "search":
                if self.distance(sample_cell_x, sample_cell_y, self.food.x, self.food.y) <= self.food.radius * 2:
                    sample_cell = (self.food.x, self.food.y)
                    value = 256
                else:
                    value = self.area.pheromone_layer.get_at(sample_cell).r
            if self.mode == "return":
                if self.distance(sample_cell_x, sample_cell_y, self.home.x, self.home.y) <= self.home.radius * 2:
                    sample_cell = (self.home.x, self.home.y)
                    value = 256
                else:
                    value = self.area.pheromone_layer.get_at(sample_cell).b
            if value != 0:
                surrounding[sample_cell] = value
        return surrounding

    def walk_random(self):
        self.direction += random.randint(-self.angle, self.angle)
        self.walk_step()

    def walk_step(self):
        self.x += cos(radians(self.direction))
        self.y += sin(radians(self.direction))
        self.bounce_border()

    def bounce_border(self):
        if self.x >= self.area.width:
            self.x = self.area.width - 1
            self.bounce_direction()
        if self.x < 0:
            self.x = 0
            self.bounce_direction()
        if self.y >= self.area.height:
            self.y = self.area.height - 1            
            self.bounce_direction()
        if self.y < 0: 
            self.y = 0
            self.bounce_direction()

    def bounce_direction(self):
        self.direction += 180
        if self.direction > 359:
            self.direction -= 360

    def spray(self):
        self.current_steps += 1
        if self.current_steps == self.steps_to_spray:
            if self.duration_to_spray > 0:
                self.duration_to_spray -= 1
                spray_intensity = int(((self.duration_to_spray / self.max_duration_to_spray) ** self.ant_spray_decrease) * self.max_spray_intensity)
                self.area.spray(int(self.x), int(self.y), self.mode, spray_intensity)
            self.current_steps = 0

    def draw(self):
        if self.mode == "search":
            self.area.ant_layer.set_at((int(self.x), int(self.y)), pygame.Color(self.color_search))
        if self.mode == "return":
            self.area.ant_layer.set_at((int(self.x), int(self.y)), pygame.Color(self.color_return))
        if self.is_debug:
            pygame.draw.circle(self.area.ant_layer, self.color_debug, (int(self.x), int(self.y)), 5.0, 1)
            