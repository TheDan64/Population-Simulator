import shared
import testsimulation

class ReflexAgent:
    # Need to add a memory of previous actions and results

    def evalFoodNeed(self, simState):
        # Determines how well the city is doing for food
        pass

    def evalProductionNeed(self, simState):
        # Determines how well the city is doing for income
        pass

    def getAction(self, simState):
        # Returns the selected tile and improvement type
        tiles = simState.getPossibleActions()

        for tile in tiles:
            pass

        return (None, None) # tmp
