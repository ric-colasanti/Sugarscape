import pygame, sys, random
from pygame.locals import *
import random as rnd
import time
from pyabm import World, Cell, Agent



pygame.init()
 
# Colours
BACKGROUND = (0, 0, 0)
RED = (255, 30, 70)
BLUE = (10, 20, 200)
GREEN = (50, 230, 40)
 
# Game Setup
FPS = 120
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
            r = int(255*(amount/value))
            if r>255:
                r=255
            if r<0:
                r=0
            pygame.draw.rect(WINDOW,(r,0,0),box)
    for agent in world.agents:
        cell = agent.getHome()
        x_pos = int(cell.x_pos*ratio+(ratio/2))
        y_pos = int(cell.y_pos*ratio+(ratio/2))
        pygame.draw.circle(WINDOW, agent.color, (x_pos,y_pos),int(box_size/2))

# The main function that controls the game
def main () :
    looping = True
    world = World(120, ["signal"],[0],n_type=4)
    # add an agent
    world.addAgent(60,60,color='red')
  
  # The main game loop
    while looping :
    # Get inputs
        for event in pygame.event.get() :
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
        
        # Processing
        for agent in world.agents:
            # what is the signle at the cell that agent occupies
            state = agent.getState("signal")
            if state == 1:
                agent.setState("signal",0)
                agent.right()
            else:
                agent.setState("signal",1)
                agent.left()
        
        # This section will be built out later
    
        # Render elements of the game
        WINDOW.fill(BACKGROUND)
        draw(world, "signal", 1,discreet=True)
        pygame.display.update()
        fpsClock.tick(FPS)
 
main()