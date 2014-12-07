"""
    This file contains a test SimulationState and Tile information.
    It was used as a sample for Dan to test the AI with various
    configurations.
"""

from shared import *
import random
import copy

map_width = 5
map_height = 5

class Tile:
    def __init__(self, position):
        self.type = random.choice([t for t in tileType])
        self.state = None
        self.position = position

        if tileType == tileType.Baren:
            self.productionRate = 0
        else:
            self.productionRate = random.randint(1, 3)

class SimulationState:
    def __init__(self):
        self.income = 0
        self.food = 0
        self.population = range(10)
        self.land = {(x, y):Tile((x,y)) for x in range(map_width) for y in range(map_height)}
        self.turn = 1

    def getPossibleActions(self):
        # Return all of the unimproved tiles
        return [tile for key, tile in self.land.items() if tile.state is None]

    def update(self, tile, improvement):
        # AI chooses its move
        if tile is not None and improvement is not None:
            self.land[tile.position].state = improvement

        for key, tile in self.land.items():
            if tile.state == tileState.Mine:
                self.income += tile.productionRate
            elif tile.state == tileState.Farm:
                self.food += tile.productionRate

        self.income -= 3 # For improvement

        # Random Event possible

        self.turn += 1

    def nextSimState(self, tile, improvement):
        state = copy.deepcopy(self)

        if tile is not None and improvement is not None:
            state.land[tile.position].state = improvement

        for key, tile in state.land.items():
            if tile.state == tileState.Mine:
                state.income += tile.productionRate
            elif tile.state == tileState.Farm:
                state.food += tile.productionRate

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

    def getTurn(self):
        return self.turn

    def getCurrentScore(self):
        # This is the score 'heuristic'
        return self.income + len(self.population) + self.food
    
