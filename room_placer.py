#!/usr/bin/env python

from support import *
import random as rand

class RoomPlacer:
  def __init__ (self):
    pass

  def place_rooms(self, map_grid, amount, size_range_and_odds):
    pass

class DefaultRoomPlacer(RoomPlacer):
  def place_rooms(self, map_grid, amount, size_range_and_odds, start_id):
    rooms = []
    for i in range(amount):
      room = self.place_room(map_grid, size_range_and_odds, len(rooms) + start_id)
      if (room != None):
        rooms.append(room)
    return rooms


  def place_room(self, map_grid, size_range_and_odds, room_id):
    odds = rand.random()
    i = 0
    odds -= size_range_and_odds[i][0]
    while (odds > 0) and (i < len(size_range_and_odds)-2):
      i += 1
      odds -= size_range_and_odds[i][0]
    size = size_range_and_odds[i][1]

    rx = rand.randint(0,len(map_grid)-size[0]-1)
    ry = rand.randint(0,len(map_grid[0])-size[1]-1)

    if ((rx + size[0]) > len(map_grid) - 1) or ((ry + size[1]) > len(map_grid[0]) - 1):
      return None # room outside the map boundaries

    for dx in range(size[0]):
      for dy in range(size[1]):
        if (map_grid[rx+dx][ry+dy].occupation != EMPTY):
          return None # room 

    #Sala tem espaço para ser construída
    tiles = []
    for dx in range(size[0]):
      for dy in range(size[1]):
        tile = map_grid[rx+dx][ry+dy]
        tile.room_id = room_id
        tile.occupation = ROOM
        if (dx < size[0] -1 ):
          tile.passages |= PASSAGE_RIGHT
        if (dx > 0):
          tile.passages |= PASSAGE_LEFT
        if (dy > 0):
          tile.passages |= PASSAGE_UP
        if (dy < size[1]-1):
          tile.passages |= PASSAGE_DOWN
        tiles.append(tile)
    room = Room(room_id, tiles)
    return room

