"""
    This file contains base code used mutually between the simulation and agent.
    Also checks to see if Enums are available when running the simulation.
"""
import logging

logging.basicConfig(format='%(levelname)s  %(message)s', level=logging.CRITICAL)

try:
    from enum import Enum
except:
    import sys

    raise Exception("You do not seem to have enums available. Enums require" +
        " either Python 3.4 or https://pypi.python.org/pypi/enum34 backport " +
        "installed manually or via pip.")

heuristic = 1

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

# Credit to UC Berkeley for the following class
class Counter(dict):
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def argMax(self):
        """
        Returns the key with the highest value.
        """
        if len(self.keys()) == 0: return None
        all = self.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]