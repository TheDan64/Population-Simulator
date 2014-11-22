import shared

class Tile:
    pass

class SimulationState:
    def __init__(self):
        self.income = 0
        self.food = 0
        self.population = []
        self.land = []

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

    
