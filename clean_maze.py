#!/usr/bin/env python

from support import *

class CleanMaze:
  def __init__(self):
    pass

  def clean(self, map_grid, clean_amount):
    '''
    Clean unnecessary corridors.
    '''
    self.grid = map_grid
    for i in range(clean_amount):
      self.visited_tiles = []
      #choose a corridor and clean it
      for corridor in map_grid.get_corridors():
        self.clean_corridor(corridor)

  def clean_corridor(self, corridor):
    # start by getting a door.
    door = None
    for tile in corridor.tiles:
      if tile.doors != DOOR_NONE:
        door = tile
        break
    # now, flood the maze, looking for useless branches
    self.flood_maze(door, [door])

  def flood_maze(self, tile, path):
    #At the start, there is no path as it is already in a door.
    self.visited_tiles.append(tile)
    if (tile.doors != DOOR_NONE):
      new_path = [tile]
    else:
      new_path = [p for p in path]

      if ( tile.passages in DEAD_ENDS):
        # a dead end - remove path
        #print("Removing tile with passage: ",tile.passages, " coord: ",tile.x,"-",tile.y, " path: ",len(new_path))
        #tile.make_wall()
        self.remove_path(tile,new_path)
        return
      elif ( tile.passages in BIFURCATION ):
        # bifurcation works as a door for us
        new_path = [tile]

    for i in range(len(DIRECTION)):
      final_path = [p for p in new_path]
      if (tile.passages&DIRECTION[i] > 0):
        new_pos = (tile.x + DELTA[i][0], tile.y + DELTA[i][1])
        new_tile = self.grid.get_grid()[new_pos[0]][new_pos[1]]
        if not (new_tile in self.visited_tiles):
          final_path.append(new_tile)
          self.flood_maze(new_tile, final_path)


      

  def remove_path(self, tile, path):
    delta = get_direction_int((path[1].x - path[0].x, path[1].y - path[0].y))
    path[0].passages &= ~DIRECTION[delta]
    #cid = len(tile.grid.get_rooms())+len(tile.grid.get_corridors())+len(tile.grid.cleanness)
    #tile.grid.cleanness.append([p for p in path])
    for tile in path[1:]:
      tile.make_wall() 
      #tile.room_id = cid


