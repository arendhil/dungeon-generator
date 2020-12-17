# dungeon-generator
Simple dungeon/maze generator in python.

This is an Dungeon/Maze generation algorithm based on some of these algorithms:
- http://journal.stuffwithstuff.com/2014/12/21/rooms-and-mazes/
- http://www.astrolog.org/labyrnth/algrithm.htm

All can be executed through:
<code>
python maze01.py
</code>

All you need is:
- Python 3.4+
- Pygame

To install all requirements with pip user:
`pip install -r REQUIREMENTS`

maze_generator.py - has the algorithms for generating the maze part (for now there is only the Recursive Backtracker)

room_placer.py - has the algorithms for placing rooms

support.py - support classes to operate the logic

map_grid.py - main class that links everything together

maze01.py - example code.

clean_maze.py - empty for now, but should take care of removing excessive dead-ends and corridors.
