"""
    This file contains base code used mutually between the simulation and agent.
    Also checks to see if Enums are available when running the simulation.
"""

try:
    from enum import Enum
except:
    import sys

    raise Exception("You do not seem to have enums available. Enums require" +
        " either Python 3.4 or https://pypi.python.org/pypi/enum34 backport " +
        "installed manually or via pip.")

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