from shared import *
import testsimulation

class ReflexAgent:
    # Possibly: Add a memory of previous actions and results
    # to affect outcome
    def evalFoodNeed(self, simState):
        # Determines how well the city is doing for food
        pass

    def evalIncomeNeed(self, simState):
        # Determines how well the city is doing for income
        pass

    def getAction(self, simState):
        # Returns the selected tile and improvement type
        tiles = simState.getPossibleActions()

        bestTile, improvement, rate = None, None, 0

        # Basic AI, picks the most productive tile
        # ToDo: picks based on current population and income
        # ToDo: check next game state to see how it is influenced
        for tile in tiles:
            if tile.productionRate > rate:
                bestTile, rate = tile, tile.productionRate

                # Baren tiles will never be picked,
                # so theres no need to check for them
                if tile.type == tileType.Both:
                    improvement = random.choice([tileState.Farm, tileState.Mine])
                elif tile.type == tileType.Farmable:
                    improvement = tileState.Farm
                elif tile.type == tileType.Mineable:
                    improvement = tileState.Mine

        return bestTile, improvement
