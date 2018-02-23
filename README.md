# dungeon-generator
Simple dungeon/maze generator in python.

This is an Dungeon/Maze generation algorithm.

All can be executed through:
<code>
python maze01.py
</code>

All you need is:
- Python 3.4+
- Pygame

maze_generator.py - has the algorithms for generating the maze part (for now there is only the Recursive Backtracker)
room_placer.py - has the algorithms for placing rooms
support.py - support classes to operate the logic
map_grid.py - main class that links everything together
maze01.py - example code.
clean_maze.py - empty for now, but should take care of removing excessive dead-ends and corridors.
