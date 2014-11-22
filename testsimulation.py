import shared
import random

map_width = 5
map_height = 5

class Tile:
    def __init__(self):
        tileType = random.choice([t for t in shared.tileType])
        tileState = None

class SimulationState:
    def __init__(self):
        self.income = 0
        self.food = 0
        self.population = []
        self.land = {(x, y):Tile() for x in range(map_width) for y in range(map_height)}

    def getPossibleActions(self):
        # Return all of the unimproved tiles
        pass

    def update(self, coord, improvement):
        # AI chooses its move
        # Random Event possible,
        # Turn counter incremented
        pass

    def nextGameState(self, position, improvement):
        
        pass

    def stillAlive(self):
        pass

    # Getters

    def getIncome(self):
        return self.income

    def getFood(self):
        return self.food

    def getPopulation(self):
        return self.population

    def getLand(self):
        return self.land

    
