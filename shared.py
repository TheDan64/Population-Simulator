from enum import Enum

# What the tile can become
class tileType(Enum):
	Farmable = 1
	Mineable = 2 
	Both = 3
	Baren = 4

# What the tile is
class tileState(Enum): 
	Farm = 1
	Mine = 2