#!/usr/bin/env python
SCREEN_SIZE = (600,600)
WHITE = (255,255,255)
BLACK = (0,0,0)
WALL_COLOR = BLACK

SHUFFLES = ( (186,186,215), (200,200,215), (160,160,215), (145,145,215), (125,125,215), (115,115,215), (95,95,215), (80,80,215) )
SHUFFLES_CORRIDOR = ( (215,125,26), (215,125,45), (215,125,60), (215,125,15), (215,125,80), (215,125,75), (215,125,95), (215,125,110) )
SHUFFLES_CLEAN = ( (20, 20, 20), (50, 20, 20), (15, 20, 20), (86, 20, 20), (125, 20, 20), (35, 20, 20), (86, 25, 25), (86, 50, 50), (50, 50, 50) )

GRID_SIZE = 30
ROOMS_AMOUNT = 50
CLEAN_INTERACTION = 10

EMPTY = 0
WALL = 1
CORRIDOR = 2
ROOM = 3
DEBUG = 999

DOOR_NONE = 0
DOOR_UP = 1
DOOR_RIGHT = 2
DOOR_DOWN = 4
DOOR_LEFT = 8

PASSAGE_NONE = 0
PASSAGE_UP = 1
PASSAGE_RIGHT = 2
PASSAGE_DOWN = 4
PASSAGE_LEFT = 8

DOORS = [DOOR_UP, DOOR_RIGHT, DOOR_DOWN, DOOR_LEFT]
DIRECTION = [PASSAGE_UP, PASSAGE_RIGHT, PASSAGE_DOWN, PASSAGE_LEFT] ## N, E, S, W
OPOSITE_DIRECTION = [PASSAGE_DOWN, PASSAGE_LEFT, PASSAGE_UP, PASSAGE_RIGHT]
DELTA = [(0,-1), (1, 0), (0, 1), (-1, 0)]

BIFURCATION = [7, 11, 13, 14, 15] #1110, 1101, 1011, 0111, 1111
CORRIDORS = [3, 5, 9, 6, 10, 12] #1100, 1010, 1001, 0110, 0101, 0011
DEAD_ENDS = [0, 1, 2, 4, 8] #0000, 1000, 0100, 0010, 0001

from random import randint

def get_direction_int(delta):
  for i in range(len(DELTA)):
    if (DELTA[i][0] == delta[0]) and (DELTA[i][1] == delta[1]):
      return i

  print("Could not reach a veredict with ",delta)
  return -1

class Tile:
  def __init__(self,x,y, map_grid):
    self.x = x
    self.y = y
    self.occupation = EMPTY
    self.room_id = -1
    self.passages = PASSAGE_NONE
    self.doors = DOOR_NONE
    self.grid = map_grid

  def __str__(self):
    print(str(self.occupation)+" - doors: "+str(self.doors))

  def make_wall(self):
    #self.occupation = DEBUG
    self.occupation = WALL
    self.room_id = -1
    self.passages = PASSAGE_NONE
    self.doors = DOOR_NONE

class Room:
  def __init__(self, room_id, tiles):
    self.room_id = room_id
    self.border_rooms = []
    self.connected_rooms = []
    self.border = []
    self.tiles = [ tile for tile in tiles]

  def close_room(self, map_grid):
    self.border = []
    self.border_rooms = []
    for tile in self.tiles:
      for i in range(len(DIRECTION)):
        if (tile.passages&DIRECTION[i] == 0):
          next_tile_pos = (tile.x + DELTA[i][0], tile.y + DELTA[i][1])
          if (Room.is_inside(next_tile_pos, map_grid)):
            next_tile = map_grid[next_tile_pos[0]][next_tile_pos[1]]
            self.border.append((tile, next_tile, i)) #room_tile, outside_tile, DIRECTION
            if not (next_tile.room_id in self.border_rooms):
              self.border_rooms.append(next_tile.room_id)

  def open_doors(self):
    reduced_border = []
    #First, look for borders that are not borders anymore - door already openned
    for tile in self.border:
      if (tile[0].doors&DOORS[tile[2]] != 0):
        #found a door, therefore a connection to another room
        if not (tile[1].room_id in self.connected_rooms):
          self.connected_rooms.append(tile[1].room_id)

    #create a border set with only the not yet connected.
    for tile in self.border:
      if not (tile[1].room_id in self.connected_rooms):
        reduced_border.append(tile)

    while len(reduced_border) > 0:
      border_tile = reduced_border[randint(0,len(reduced_border)-1)]
      border_tile[0].doors |= DIRECTION[border_tile[2]]
      border_tile[1].doors |= OPOSITE_DIRECTION[border_tile[2]]
      new_border = []
      for tile in reduced_border:
        if (tile[1].room_id != border_tile[1].room_id):
          new_border.append(tile)
      reduced_border = new_border
      self.connected_rooms.append(border_tile[1].room_id)
    #print( (self.room_id, len(self.border_rooms), len(self.connected_rooms) ) )

  def is_inside(pos, grid):
    return ( (pos[0] >= 0) and (pos[1] >= 0) and \
             (pos[0] < len(grid)) and (pos[1] < len(grid[0])) )

class Corridor:
  def __init__(self, corridor_id):
    self.tiles = []
    self.corridor_id = corridor_id

  def add_tile(self, tile):
    self.tiles += [tile]
