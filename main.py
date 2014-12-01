#! /usr/bin/env python3

from agent import *
from simulation import *
import logging
import random
import sys

def main():
    
    logging.basicConfig(format='%(levelname)s  %(message)s', level=logging.DEBUG)
    turn = 0

    # Generate a randomized starting simulation
    simulationState = SimulationState()
    agent = ReflexAgent()
    tile = simulationState.getPossibleActions()[1]
    upgrade = shared.tileState.Farm
    # Testing nextGameState
    # print(simulationState.nextGameState(tile, upgrade).land[tile.position].state)
    # print(simulationState.update(tile, shared.tileState.Farm))

    while True:
        # Break when theres no moves left for now
        if not simulationState.stillAlive():
            break
        # Ignore AI, just step manually with no improvements for now
        # tile, upgrade = agent.getAction(simulationState)
        # simulationState.update(tile, upgrade)
        input("\nOn turn " + str(turn) + " Press Enter to continue...")
        turn = turn + 1
        simulationState.update(None, None)


# Call main fn when running this script (as opposed to importing it)
if __name__ == "__main__":
    main()