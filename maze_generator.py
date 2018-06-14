#!/usr/bin/env python

from support import *
import random as rand

class MazeGenerator:

  def generate(self, map_grid, tiles_list, start_id):
    pass


class RecursiveBacktrackerMaze(MazeGenerator):

  def generate(self, map_grid, tiles_list, start_id):
    corridors = []
    self.possible_tiles = [ item for item in tiles_list ]
    # print("Drawing mazes with "+str(len(self.possible_tiles))+" tiles.")
    # print("First tile: "+str(new_tile.x)+", "+str(new_tile.y))
    while len(self.possible_tiles) > 0:
      new_tile = map_grid[self.possible_tiles[0][0]][self.possible_tiles[0][1]]
      new_corridor = Corridor(len(corridors) + start_id)
      self._walk_through(map_grid, new_tile, new_corridor)
      corridors.append(new_corridor)
    return corridors

  def _walk_through(self, map_grid, tile, corridor):
    self.possible_tiles.remove((tile.x, tile.y))
    corridor.add_tile(tile)
    tile.occupation = CORRIDOR
    tile.room_id = corridor.corridor_id
    directions = [0,1,2,3]
    rand.shuffle(directions)
    while len(directions) > 0 :
      ndir = directions.pop()
      pos = (tile.x + DELTA[ndir][0], tile.y + DELTA[ndir][1])
      if (pos in self.possible_tiles):
        tile.passages |= DIRECTION[ndir]
        new_tile = map_grid[pos[0]][pos[1]]
        new_tile.passages |= OPOSITE_DIRECTION[ndir]
        self._walk_through(map_grid, new_tile, corridor)


class DirectConnection(MazeGenerator):
  def generate(self, map_grid, tiles_list, start_id):
    pass
