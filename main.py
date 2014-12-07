#! /usr/bin/env python3

"""
    This file contains the main loop to get the Agent and Environment working
    together. Also takes care of user input to pause or proceed with the
    simulation.
"""

from agent import *
from simulation import *

def printStatistics(simState):
    print("""Town Statistics
    Population:  {}
    Food:        {}
    Income:      {}
    Total Score: {}\
""".format(len(simState.getPopulation()), simState.getFood(),
    simState.getIncome(), simState.getCurrentScore()))

def main():
    # Generate a randomized starting simulation
    simState = SimulationState(5, 5, 100, 100)
    agent = ReflexAgent()
    skipInputTurns = 0

    # End when theres no moves left or population is dead
    while simState.stillAlive() and simState.getTurn() <= 25:

        if not skipInputTurns:
            # Get player input if skipInputTurns == 0
            inp = input("Press a command followed by enter: ")
        
            # If an integer, proceed for int # of terms
            try:
                skipInputTurns = int(inp)
            except ValueError:
                if inp == 'e':
                    exit()
                elif inp == 'p':
                    printStatistics(simState)

        tile, improvement = agent.getAction(simState)

        if tile is None:
            print("Turn {:3}: The Govenor does nothing this turn.".format(simState.getTurn()))
        else:
            print("Turn {:3}: The Govenor creates a new {} for the town.".format(simState.getTurn(), improvement.name))

        simState.update(tile, improvement)

        if skipInputTurns > 0:
            skipInputTurns -= 1
    printStatistics(simState)

# Call main fn when running this script (as opposed to importing it)
if __name__ == "__main__":
    main()