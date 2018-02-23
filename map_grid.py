#!/usr/bin/env python

from support import *
from maze_generator import *
from room_placer import *

class MapGrid:
  
  def __init__(self, size, rooms_amount):
    self.__size = size
    self.__rooms = []
    self.__corridors = []
    self.generate_grid()
    self.create_maze(rooms_amount)
    self.close_and_clean_maze()

  def generate_grid(self):
    # start with a blank grid
    self.__grid = []
    for x in range(self.__size[0]//10):
      line = []
      for y in range(self.__size[1]//10):
        new_tile = Tile(x,y, self)
        line += [new_tile]
      self.__grid += [line]

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

  def get_grid(self):
    return self.__grid

  def get_rooms(self):
    return self.__rooms

  def get_corridors(self):
    return self.__corridors
