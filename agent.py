"""
    This file contains the actual agent implementation. Has a Memory class for
    keeping track of previously similar actions.
"""

from shared import *
import testsimulation
import random

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

            logging.basicConfig(format='%(levelname)s  %(message)s', level=logging.CRITICAL)

            for i in improvements:
                nextState = simState.nextGameState(tile, i)

                # Check the next state that would be produced
                if nextState.getCurrentScore() > score or \
                    self.memory.check((simState.getCurrentScore(), tile.type, i)) > score:
                    
                    bestTile, improvement = tile, i

                    score = nextState.getCurrentScore()

            logging.basicConfig(format='%(levelname)s  %(message)s', level=logging.DEBUG)


        type_ = bestTile.type if bestTile is not None else None

        self.memory.add((simState.getCurrentScore(), type_, improvement))

        return bestTile, improvement

class QLearningAgent:
    def __init__(self, alpha, epsilon, gamma):
        self.qValues = Counter()
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma

    def updateAlpha(self, alpha):
        self.alpha = alpha

    def updateEpsilon(self, epsilon):
        self.epsilon = epsilon

    def generateImprovements(self, tile):
        improvements = []

        if tile.type == tileType.Both:
            improvements = [tileState.Farm, tileState.Mine]
        elif tile.type == tileType.Farmable:
            improvements = [tileState.Farm]
        elif tile.type == tileType.Mineable:
            improvements = [tileState.Mine]

        return improvements

    def getQValue(self, state, action):
        return self.qValues[(state, action)]

    def getValue(self, simState):
        tiles = simState.getPossibleActions()

        if not len(tiles):
            return 0.0

        value = -float("inf")

        for tile in tiles:
            improvements = self.generateImprovements(tile)

            for i in improvements:
                newValue = self.getQValue(tile.position, i)
                
                if newValue > value:
                    value = newValue

        if value == -float("inf"):
            return -100

        return value

    def getPolicy(self, simState):
        tiles = simState.getPossibleActions()

        if not len(tiles):
            return None, None

        value, bestTile, bestImprovement = -float("inf"), None, None

        for tile in tiles:
            improvements = self.generateImprovements(tile)

            for i in improvements:
                newValue = self.getQValue(tile.position, i)

                if newValue > value:
                    value = newValue
                    bestTile = tile
                    bestImprovement = i

        return bestTile, bestImprovement

    def getAction(self, simState):
        tiles = simState.getPossibleActions()
        action, tile = None, None

        if not len(tiles):
            return None, None

        if random.random() < self.epsilon:
            tile = random.choice(tiles)

            if tile.type == tileType.Baren:
                tile, action = None, None
            else:
                action = random.choice(self.generateImprovements(tile))
        else:
            tile, action = self.getPolicy(simState)

        return tile, action

    # Standard Q-value update fn
    def update(self, state, action, nextState, reward):
        newQValue = reward + self.gamma * self.getValue(nextState)

        self.qValues[(state, action)] = (1 - self.alpha) * self.getQValue(state, action) + self.alpha * newQValue