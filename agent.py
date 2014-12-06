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
        self.memories = {} 

    # Add the memory of what you did
    def add(self, score, tileType, improvement):
        self.queue.append((score, tileType, improvement))

    # Update the memory of what you did to the resulting turn's score
    def update(self, newScore):
        if len(self.queue) > 0:
            score, tileType, improvement = self.queue.pop(0)

            # ToDo: if self.memories[...] already exists, update it with the
            # average of the two?
            self.memories[(score, tileType, improvement)] = newScore

    # Find out the resulting score from memory
    def check(self, score, tileType, improvement):
        # Return the memory if it exists
        try:
            return self.memories[(score, tileType, improvement)]

        # If the memory doesn't exist, return a bad value
        except:
            return -float("inf")

class ReflexAgent:
    def __init__(self):
        # Remembers previous actions and situations to improve its own
        self.memory = Memory()

    def getAction(self, simState):
        self.memory.update(simState.getCurrentScore())

        # Returns the selected tile and improvement type
        tiles = simState.getPossibleActions()

        bestTile, improvement, score = None, None, 0

        # Reflex AI, picks the most productive tile
        # based on how the next state will be (not inc random events)

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
                nextState = simState.nextSimState(tile, i)

                # Check the next state that would be produced
                if nextState.getCurrentScore() > score or \
                    self.memory.check(simState.getCurrentScore(), tile.type, i) > score:
                    
                    bestTile, improvement = tile, i

                    score = nextState.getCurrentScore()

        # Check if no action is the best action
        nextState = simState.nextSimState(None, None)

        if nextState.getCurrentScore() > score:
            bestTile, improvement = None, None

        type_ = bestTile.type if bestTile is not None else None

        self.memory.add(simState.getCurrentScore(), type_, improvement)

        return bestTile, improvement
