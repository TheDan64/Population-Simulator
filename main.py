#! /usr/bin/env python3

"""
    This file contains the main loop to get the Agent and Environment working
    together. Also takes care of user input to pause or proceed with the
    simulation.
"""

from agent import *
from testsimulation import *

def printStatistics(simState):
    print("""Town Statistics
\tPopulation:  {}
\tFood:        {}
\tIncome:      {}
\tTotal Score: {}
""".format(len(simState.getPopulation()), simState.getFood(),
    simState.getIncome(), simState.getCurrentScore()))

def main():
    # Generate a randomized starting simulation
    simState = SimulationState()
    agent = ReflexAgent()

    while True:
        # Break when theres no moves left for now
        if not simState.stillAlive() or simState.getTurn() == 25:
            break

        tile, improvement = agent.getAction(simState)

        if tile is None:
            print("Turn {:3}: The Govenor does nothing this turn.".format(simState.getTurn()))
        else:
            print("Turn {:3}: The Govenor creates a new {} for the town.".format(simState.getTurn(), improvement.name))

        simState.update(tile, improvement)

        #printStatistics(simState)

# Call main fn when running this script (as opposed to importing it)
if __name__ == "__main__":
    main()