"""
    This file contains the actual agent implementation. Has a Memory class for
    keeping track of previously similar actions.
"""

from shared import *
import testsimulation

# Remembers previous actions and results (including random events)
class Memory:
    def __init__(self):
        # A queue to associate your previous action with the current
        # (resulting) score
        self.queue = [] 

        # Associate current score, tile type, and improvement to future score
        # (score, tile type, improvement) : score
        self.history = {} 

    # Add the memory of what you did
    def add(self, scoreTypeImprovement):
        self.queue.append(scoreTypeImprovement)

    # Update the memory of what you did to the resulting turn's score
    def update(self, newScore):
        if len(self.queue) > 0:
            scoreTypeImprovement = self.queue.pop(0)

            # If it already exists, average the two memories
            if scoreTypeImprovement in self.history:
                self.history[scoreTypeImprovement] += newScore
                self.history[scoreTypeImprovement] /= 2

            # Otherwise just create a new memory
            else:
                self.history[scoreTypeImprovement] = newScore

    # Find out the resulting score from memory
    def check(self, scoreTypeImprovement):
        # Return the memory if it exists
        if scoreTypeImprovement in self.history:
            return self.history[scoreTypeImprovement]

        # If the memory doesn't exist, return a bad value
        else:
            return -float("inf")

class ReflexAgent:
    def __init__(self):
        # Remembers previous actions and situations to improve its own
        self.memory = Memory()

    def getAction(self, simState):
        self.memory.update(simState.getCurrentScore())

        # Returns the selected tile and improvement type
        tiles = simState.getPossibleActions()

        # Initialize and initialize default action to no action
        bestTile, improvement = None, None
        score = simState.nextGameState(None, None).getCurrentScore()

        # Reflex AI, picks the most productive tile
        # based on how the next state will be or whether having made
        # the same action previously we beneficial

        for tile in tiles:
            improvements = []

            # Make a list of possible improvements relative to the current tile
            if tile.type == tileType.Both:
                improvements = [tileState.Farm, tileState.Mine]
            elif tile.type == tileType.Farmable:
                improvements = [tileState.Farm]
            elif tile.type == tileType.Mineable:
                improvements = [tileState.Mine]           

            # Find the improvement that yields the greatest score            
            for i in improvements:
                nextState = simState.nextGameState(tile, i)

                # Check the next state that would be produced
                if nextState.getCurrentScore() > score or \
                    self.memory.check((simState.getCurrentScore(), tile.type, i)) > score:
                    
                    bestTile, improvement = tile, i

                    score = nextState.getCurrentScore()

        type_ = bestTile.type if bestTile is not None else None

        self.memory.add((simState.getCurrentScore(), type_, improvement))

        return bestTile, improvement
