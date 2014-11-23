try:
    from enum import Enum
except:
    import sys

    print("""You do not seem to have enums available.
Enums require either Python 3.4 or
https://pypi.python.org/pypi/enum34 backport installed
manually or via pip.
    - Dan""")

    sys.exit()

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