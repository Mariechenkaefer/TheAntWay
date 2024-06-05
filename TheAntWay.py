import pygame
from area import Area
from food import Food
from home import Home

pygame.init()

my_area = Area(width = 1000, height = 750, caption = "The Ant Way", 
               spray_decrease_ticks = 10)
my_food = Food(my_area, 
               x = 200, y = 150, radius = 10)
my_home = Home(my_area, my_food, 
               x = 300, y = 350, radius = 12, 
               ant_count = 1000, 
               ant_max_spray_intensity = 255, ant_max_duration_to_spray = 7000, 
               ant_steps_to_spray = 3, ant_spray_decrease = 200, 
               ant_steps_to_ignore = 3, ant_surrounding_angle = 30, ant_angle = 15, 
               sample_count = 50, sample_min_length = 3, sample_max_length = 10,
               ant_color_search = "lightgoldenrodyellow", ant_color_return = "darkorange")

run = True 
while run: 
  my_area.tick()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

pygame.quit()
