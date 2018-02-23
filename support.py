#!/usr/bin/env python
EMPTY = 0
WALL = 1
CORRIDOR = 2
ROOM = 3

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

DIRECTION = [PASSAGE_UP, PASSAGE_RIGHT, PASSAGE_DOWN, PASSAGE_LEFT] ## N, E, S, W
OPOSITE_DIRECTION = [PASSAGE_DOWN, PASSAGE_LEFT, PASSAGE_UP, PASSAGE_RIGHT]
DELTA = [(0,-1), (1, 0), (0, 1), (-1, 0)]

from random import randint

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
    print("Room %i has %i neighbours"%(self.room_id,len(self.border_rooms)))

  def open_doors(self):
    while len(self.border) > 0:
      border_tile = self.border[randint(0,len(self.border)-1)]
      border_tile[0].passages |= DIRECTION[border_tile[2]]
      border_tile[1].passages |= OPOSITE_DIRECTION[border_tile[2]]
      new_border = []
      for tile in self.border:
        if (tile[0].room_id != border_tile[0].room_id):
          new_border.append(tile)
      self.border = new_border
      self.connected_rooms.append(border_tile[1].room_id)

  def is_inside(pos, grid):
    return ( (pos[0] >= 0) and (pos[1] >= 0) and \
             (pos[0] < len(grid)) and (pos[1] < len(grid[0])) )

class Corridor:
  def __init__(self, corridor_id):
    self.tiles = []
    self.corridor_id = corridor_id

  def add_tile(self, tile):
    self.tiles += [tile]
