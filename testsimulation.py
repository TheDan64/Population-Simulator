"""
    This file contains a test SimulationState and Tile information.
    It was used as a sample for Dan to test the AI with various
    configurations.
"""

import shared
import random
import copy

map_width = 5
map_height = 5

class Tile:
    def __init__(self, position):
        self.type = random.choice([t for t in shared.tileType])
        self.state = None
        self.position = position

        if shared.tileType == shared.tileType.Baren:
            self.productionRate = 0
        else:
            self.productionRate = random.randint(1, 3)

class SimulationState:
    def __init__(self):
        self.income = 0
        self.food = 0
        self.population = range(10)
        self.land = {(x, y):Tile((x,y)) for x in range(map_width) for y in range(map_height)}

    def getPossibleActions(self):
        # Return all of the unimproved tiles
        return [tile for key, tile in self.land.items() if tile.state is None]

    def update(self, tile, improvement):
        # AI chooses its move
        if tile is not None and improvement is not None:
            self.land[tile.position].state = improvement

        for key, tile in self.land.items():
            if tile.state is not None:
                self.income += tile.productionRate

        self.income -= 3 # For improvement

        # Random Event possible

        # Turn counter incremented? Either here or in main loop

    def nextSimState(self, tile, improvement):
        state = copy.deepcopy(self)

        if tile is not None and improvement is not None:
            state.land[tile.position].state = improvement

        for key, tile in state.land.items():
            if tile.state is not None:
                state.income += tile.productionRate

        state.income -= 3 # For improvement

        return state

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

    def getCurrentScore(self):
        return self.income + len(self.population)
    
