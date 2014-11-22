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
        self.land = {t:Tile() for t in zip(range(map_width), range(map_height))}

    def getPossibleActions():
        # Return all of the unimproved tiles
        pass

    def update(coord, improvement):
        # AI chooses its move
        # Random Event possible,
        # Turn counter incremented
        pass

    def nextGameState(position, improvement):
        
        pass

    def stillAlive():
        pass

    # Getters

    def getIncome():
        return self.income

    def getFood():
        return self.food

    def getPopulation():
        return self.population

    def getLand():
        return self.land

    
