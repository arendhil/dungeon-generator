#!/usr/bin/env python
import pygame,sys
from pygame.locals import *
from map_grid import *

sys.setrecursionlimit(15000)


def draw_grid(grid):
  for x in range(len(grid)):
    for y in range(len(grid[x])):
      draw_tile(grid[x][y])

def draw_tile(tile):
  if (tile.occupation == WALL):
    pygame.draw.rect(DISPLAYSURF, WALL_COLOR, (tile.x * GRID_SIZE, tile.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
  else:
    if (tile.occupation == ROOM):
      pygame.draw.rect(DISPLAYSURF, SHUFFLES[tile.room_id % len(SHUFFLES)], (tile.x * GRID_SIZE, tile.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    elif (tile.occupation == CORRIDOR):
      pygame.draw.rect(DISPLAYSURF, SHUFFLES_CORRIDOR[tile.room_id % len(SHUFFLES)], (tile.x * GRID_SIZE, tile.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    elif (tile.occupation == DEBUG):
      pygame.draw.rect(DISPLAYSURF, SHUFFLES_CLEAN[tile.room_id % len(SHUFFLES_CLEAN)], (tile.x * GRID_SIZE, tile.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    if (tile.passages&PASSAGE_LEFT == 0):
      if (tile.doors&DOOR_LEFT != 0):
        pygame.draw.line(DISPLAYSURF, WHITE, (tile.x * GRID_SIZE -1, tile.y * GRID_SIZE -1), (tile.x * GRID_SIZE -1, tile.y * GRID_SIZE -1 + GRID_SIZE), 1)
      else:
        pygame.draw.line(DISPLAYSURF, BLACK, (tile.x * GRID_SIZE -1, tile.y * GRID_SIZE -1), (tile.x * GRID_SIZE -1, tile.y * GRID_SIZE -1 + GRID_SIZE), 1)

    if (tile.passages&PASSAGE_UP == 0):
      if (tile.doors&DOOR_UP != 0):
        pygame.draw.line(DISPLAYSURF, WHITE, (tile.x * GRID_SIZE -1, tile.y * GRID_SIZE -1), (tile.x * GRID_SIZE -1 + GRID_SIZE, tile.y * GRID_SIZE -1), 1)
      else:
        pygame.draw.line(DISPLAYSURF, BLACK, (tile.x * GRID_SIZE -1, tile.y * GRID_SIZE -1), (tile.x * GRID_SIZE -1 + GRID_SIZE, tile.y * GRID_SIZE -1), 1)

    if (tile.passages&PASSAGE_RIGHT == 0):
      if (tile.doors&DOOR_RIGHT != 0):
        pygame.draw.line(DISPLAYSURF, WHITE, (tile.x * GRID_SIZE -1 + GRID_SIZE, tile.y * GRID_SIZE -1), (tile.x * GRID_SIZE -1 + GRID_SIZE, tile.y * GRID_SIZE -1 + GRID_SIZE), 1)
      else:
        pygame.draw.line(DISPLAYSURF, BLACK, (tile.x * GRID_SIZE -1 + GRID_SIZE, tile.y * GRID_SIZE -1), (tile.x * GRID_SIZE -1 + GRID_SIZE, tile.y * GRID_SIZE -1 + GRID_SIZE), 1)

    if (tile.passages&PASSAGE_DOWN == 0):
      if (tile.doors&DOOR_DOWN != 0):
        pygame.draw.line(DISPLAYSURF, WHITE, (tile.x * GRID_SIZE -1, tile.y * GRID_SIZE -1 + GRID_SIZE), (tile.x * GRID_SIZE -1 + GRID_SIZE, tile.y * GRID_SIZE -1 + GRID_SIZE), 1)
      else:
        pygame.draw.line(DISPLAYSURF, BLACK, (tile.x * GRID_SIZE -1, tile.y * GRID_SIZE -1 + GRID_SIZE), (tile.x * GRID_SIZE -1 + GRID_SIZE, tile.y * GRID_SIZE -1 + GRID_SIZE), 1)

def save_map(map):
  import json
  simple_map = {'screen_size': map.get_size()}
  simple_map["grid"] = map.full_grid()
  
  with open("save_map.json","w") as fdp:
    fdp.write(json.dumps(simple_map))


pygame.init()
DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Maze Generator v.0.01")

map = MapGrid(SCREEN_SIZE, ROOMS_AMOUNT, CLEAN_INTERACTION)

while True: #main loop
  for event in pygame.event.get():
    if (event.type == QUIT):
      pygame.quit()
      sys.exit()
    if (event.type == pygame.KEYDOWN):
      if (event.key == pygame.K_SPACE):
        map = MapGrid(SCREEN_SIZE, ROOMS_AMOUNT, CLEAN_INTERACTION)
      if (event.key == pygame.K_s):
        save_map(map)
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

