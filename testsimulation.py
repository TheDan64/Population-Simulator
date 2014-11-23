import shared
import random

map_width = 5
map_height = 5

class Tile:
    def __init__(self, position):
        self.type = random.choice([t for t in shared.tileType])
        self.state = None
        self.productionRate = random.randint(1, 3)
        self.position = position

class SimulationState:
    def __init__(self):
        self.income = 0
        self.food = 0
        self.population = []
        self.land = {(x, y):Tile((x,y)) for x in range(map_width) for y in range(map_height)}

    def getPossibleActions(self):
        # Return all of the unimproved tiles
        return [tile for key, tile in self.land.items() if tile.tileState is None]

    def update(self, tile, improvement):
        # AI chooses its move
        self.land[tile.position].tileState = improvement

        for tile in self.land:
            if tile.state is not None:
                self.income += tile.productionRate

        # Random Event possible

        # Turn counter incremented? Either here or in main loop

    def nextGameState(self, tile, improvement):
        pass

    def stillAlive(self):
        return len(self.population) > 0 # and other condition

    # Getters
    def getIncome(self):
        return self.income

    def getFood(self):
        return self.food

    def getPopulation(self):
        return self.population

    def getLand(self):
        return self.land

    
