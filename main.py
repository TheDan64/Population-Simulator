#! /usr/bin/env python3

"""
    This file contains the main loop to get the Agent and Environment working
    together. Also takes care of user input to pause or proceed with the
    simulation.
"""

from agent import *
from testsimulation import *

def main():
    # Generate a randomized starting simulation
    simulationState = SimulationState()
    agent = ReflexAgent()
    turn = 0

    while True:
        # Break when theres no moves left for now
        if not simulationState.stillAlive() or turn == 25:
            break

        tile, improvement = agent.getAction(simulationState)

        if tile is None:
            print("Turn {:3}: No tile picked".format(turn))
        else:
            print("Turn {:3}: The Govenor creates a new {} for the town.".format(turn, improvement.name))

        simulationState.update(tile, improvement)
        turn += 1

# Call main fn when running this script (as opposed to importing it)
if __name__ == "__main__":
    main()