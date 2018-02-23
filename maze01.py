#!/usr/bin/env python
import pygame,sys
from pygame.locals import *
from map_grid import *

sys.setrecursionlimit(15000)
SCREEN_SIZE = (400,400)
WHITE = (255,255,255)
BLACK = (0,0,0)

SHUFFLES = ( (186,186,215), (200,200,215), (160,160,215), (145,145,215), (125,125,215), (115,115,215), (95,95,215), (80,80,215) )
SHUFFLES_CORRIDOR = ( (215,125,26), (215,125,45), (215,125,60), (215,125,15), (215,125,80), (215,125,75), (215,125,95), (215,125,110) )

GRID_SIZE = 10
ROOMS_AMOUNT = 50


def draw_grid(grid):
  for x in range(len(grid)):
    for y in range(len(grid[x])):
      draw_tile(grid[x][y])

def draw_tile(tile):
  if (tile.occupation == WALL):
    pygame.draw.rect(DISPLAYSURF, BLACK, (tile.x * GRID_SIZE, tile.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

  else:
    if (tile.occupation == ROOM):
      pygame.draw.rect(DISPLAYSURF, SHUFFLES[tile.room_id % len(SHUFFLES)], (tile.x * GRID_SIZE, tile.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    if (tile.occupation == CORRIDOR):
      pygame.draw.rect(DISPLAYSURF, SHUFFLES_CORRIDOR[tile.room_id % len(SHUFFLES)], (tile.x * GRID_SIZE, tile.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    if (tile.passages&PASSAGE_LEFT == 0):
      pygame.draw.line(DISPLAYSURF, BLACK, (tile.x * GRID_SIZE -1, tile.y * GRID_SIZE -1), (tile.x * GRID_SIZE -1, tile.y * GRID_SIZE -1 + GRID_SIZE), 1)

    if (tile.passages&PASSAGE_UP == 0):
      pygame.draw.line(DISPLAYSURF, BLACK, (tile.x * GRID_SIZE -1, tile.y * GRID_SIZE -1), (tile.x * GRID_SIZE -1 + GRID_SIZE, tile.y * GRID_SIZE -1), 1)


pygame.init()
DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Maze Generator v.0.01")

map = MapGrid(SCREEN_SIZE, ROOMS_AMOUNT)

while True: #main loop
  for event in pygame.event.get():
    if (event.type == QUIT):
      pygame.quit()
      sys.exit()
    if (event.type == pygame.KEYDOWN):
      if (event.key == pygame.K_SPACE):
        map = MapGrid(SCREEN_SIZE, ROOMS_AMOUNT)
    if (event.type == pygame.MOUSEBUTTONDOWN):
      click_pos = event.pos
      click_pos = (click_pos[0]//GRID_SIZE, click_pos[1]//GRID_SIZE)
      tile = map.get_grid()[click_pos[0]][click_pos[1]]
      room_id = tile.room_id
      if (tile.occupation == ROOM):
        print("This is the room %i of %i with %i neighbours"%(tile.room_id, len(tile.grid.get_rooms()), len(tile.grid.get_rooms()[tile.room_id].border_rooms)))
        print("ids = ",tile.grid.get_rooms()[tile.room_id].border_rooms)
        
      
  DISPLAYSURF.fill(WHITE)
  draw_grid(map.get_grid())
  pygame.display.update()

