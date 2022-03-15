import math
import pygame, sys, random
from pygame.locals import *
import random as rnd
import time
from pyabm import World, Cell, Agent



pygame.init()
 
# Colours
BACKGROUND = (255, 255, 255)
RED = (255, 30, 70)
BLUE = (10, 20, 200)
GREEN = (50, 230, 40)
 
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Sugarscape-01')

def draw(world,state,value,discreet=False):
    width = WINDOW_WIDTH
    ratio = width/world.size
    box_size = int(ratio-1)
    
    for cell in world.cells:
        x_pos = int(cell.x_pos*ratio)
        y_pos = int(cell.y_pos*ratio)
        box = pygame.Rect((x_pos,y_pos),(box_size,box_size))
        if discreet:
            if cell.isState(state,value):
              pygame.draw.rect(WINDOW, GREEN, box)
        else:
            amount = cell.getState(state)
            r = 255-int(255*(amount/value))
            if r>255:
                r=255
            if r<0:
                r=0
            pygame.draw.rect(WINDOW,(255,255,r),box)
    for agent in world.agents:
        cell = agent.getHome()
        x_pos = int(cell.x_pos*ratio+(ratio/2))
        y_pos = int(cell.y_pos*ratio+(ratio/2))
        pygame.draw.circle(WINDOW, agent.color, (x_pos,y_pos),int(box_size/2))

# The main function that controls the game
def main () :
  looping = True

  world = World(50, ["sugar","sugar-capacity"],[0,0],n_type=4)
  #set center cell sugar to 500
  world.setCell(13, 13, "sugar", 4)
  for cell in world.cells:
      value1 = ((25-math.sqrt(math.pow((cell.x_pos-32),2)+math.pow((cell.y_pos-13),2)))/5)
      if value1<0 : value1=0
      value2 = ((25-math.sqrt(math.pow((cell.x_pos-13),2)+math.pow((cell.y_pos-32),2)))/5)
      if value2<0 : value2=0
      cell.setState("sugar",max(value1,value2))
      cell.setAState("sugar-capacity",max(value1,value2))
  world.update()
  sugar_update = 1
  for _ in range(40):
    world.addAgent(rnd.randint(0,49),rnd.randint(0,49),color='red',vision=rnd.randint(1,3))
  
  # The main game loop
  while looping :
    # Get inputs
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()
    
    # Processing
    #world.diffuse("sugar",0.5)
    for agent in world.agents:
        res = agent.getState("sugar")
        if res >= agent.vision:
            res -= agent.vision
            agent.setState("sugar",res)
            agent.moveBest("sugar")
    for cell in world.cells:
        value = cell.getState("sugar")
        c_value = cell.getState("sugar-capacity")
        cell.setState("sugar",min(value+sugar_update,c_value))
    

    #pos = world.getCell(15,15)
    #print(pos.getState("sugar"))
    
    # This section will be built out later
 
    # Render elements of the game
    world.update()
    WINDOW.fill(BACKGROUND)
    draw( world, "sugar", 4,discreet=False)
    pygame.display.update()
    fpsClock.tick(FPS)
 
main()