#!/usr/bin/env python

from support import *
from maze_generator import *
from room_placer import *
from clean_maze import *

class MapGrid:

  def get_size(self):
    return self.__size
  
  def __init__(self, size, rooms_amount, clean_amount):
    self.__size = size
    self.__rooms = []
    self.__corridors = []
    #self.cleanness = []
    self.clean_amount = clean_amount
    self.generate_grid()
    self.create_maze(rooms_amount)
    self.close_and_clean_maze()

  def generate_grid(self):
    # start with a blank grid
    self.__grid = []
    for x in range(self.__size[0]//GRID_SIZE):
      line = []
      for y in range(self.__size[1]//GRID_SIZE):
        new_tile = Tile(x,y, self)
        line += [new_tile]
      self.__grid += [line]

  def full_grid(self):
    ## 0 - Empty
    ## 1 - ground
    ## 2 - wall
    ## 3 - door
    ## Zerar a grid a retornar
    grid = [ [ 0 for y in range((self.__size[1]*2)//GRID_SIZE)] for x in range((self.__size[0]*2)//GRID_SIZE)]
    
    for x in range(self.__size[0]//GRID_SIZE):
      for y in range(self.__size[1]//GRID_SIZE):
        ## Montar a máscara
        mask = [ [0 for i in range(3)] for j in range(3)]
        tile = self.__grid[x][y]
        if tile.occupation != WALL:
          ## if it is not a wall, the center is accessible
          grid[x*2+1][y*2+1] = 1
          if tile.occupation == CORRIDOR:
            if (tile.passages&PASSAGE_LEFT) != 0:
              grid[x*2][y*2+1] = 1
            if (tile.passages&PASSAGE_UP) != 0:
              grid[x*2+1][y*2] = 1
            if (tile.passages&PASSAGE_RIGHT) != 0:
              grid[x*2+2][y*2+1] = 1
            if (tile.passages&PASSAGE_DOWN) != 0:
              grid[x*2+1][y*2+2] = 1
              mask[1][2] = 1
          else:
            ## if this is a room, cover with ground first
            for i in range(3):
              for j in range(3):
                if grid[x*2+i][y*2+j] == 0:
                  grid[x*2+i][y*2+j] = 1
            mask = [ [1 for i in range(3)] for j in range(3)]

            ##Now, place the wall
            if (tile.passages&PASSAGE_LEFT) == 0:
              grid[x*2][y*2+0] = 2
              grid[x*2][y*2+1] = 2
              grid[x*2][y*2+2] = 2
            if (tile.passages&PASSAGE_UP) == 0:
              grid[x*2+0][y*2+0] = 2
              grid[x*2+1][y*2+0] = 2
              grid[x*2+2][y*2+0] = 2
            if (tile.passages&PASSAGE_RIGHT) == 0:
              grid[x*2+2][y*2+0] = 2
              grid[x*2+2][y*2+1] = 2
              grid[x*2+2][y*2+2] = 2
            if (tile.passages&PASSAGE_DOWN) == 0:
              grid[x*2+0][y*2+2] = 2
              grid[x*2+1][y*2+2] = 2
              grid[x*2+2][y*2+2] = 2

            ## if this tile has a door, override the correspondent wall tile
            if (tile.doors != 0):
              if (tile.doors&DOOR_LEFT) != 0:
                grid[x*2][y*2+1] = 3
              if (tile.doors&DOOR_UP) != 0:
                grid[x*2+1][y*2+0] = 3
              if (tile.doors&DOOR_RIGHT) != 0:
                grid[x*2+2][y*2+1] = 3
              if (tile.doors&DOOR_DOWN) != 0:
                grid[x*2+1][y*2+2] = 3
          
        ## Aplicar a máscara do Tile na grid
        # for xi in range(3):
        #   for yi in range(3):
        #     grid[x*2+xi][y*2+yi] += mask[xi][yi]
    return grid

    
  def create_maze(self, rooms_amount):
    roomsPlacer = DefaultRoomPlacer()
    rooms_odds = ((0.2,(3,3)), (0.3, (4,3)), (0.3,(3,4)), (0.2,(2,2)))
    self.__rooms = roomsPlacer.place_rooms(self.__grid, rooms_amount, rooms_odds, 0)
    
    maze = RecursiveBacktrackerMaze()
    tiles_list = []
    for x in range(len(self.__grid)):
      for y in range(len(self.__grid[x])):
        if (self.__grid[x][y].occupation == EMPTY):
          tiles_list.append((x,y))
    self.__corridors = maze.generate(self.__grid, tiles_list, len(self.__rooms))

  def close_and_clean_maze(self):
    for room in self.__rooms:
      room.close_room(self.__grid)
      room.open_doors()
    cleaner = CleanMaze()
    cleaner.clean(self, self.clean_amount)

  def get_grid(self):
    return self.__grid

  def get_rooms(self):
    return self.__rooms

  def get_corridors(self):
    return self.__corridors
