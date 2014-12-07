#! /usr/bin/env python3

"""
    This file contains the main loop to get the Agent and Environment working
    together. Also takes care of user input to pause or proceed with the
    simulation.
"""

from agent import *
from simulation import *
import logging

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
    simState = SimulationState()
    agent = ReflexAgent()
    turn = 1

    # End when theres no moves left or population is dead
    while simState.stillAlive() and turn <= 25:
        # Get player input
#        inp = input("Press a command followed by enter: ")
        
#        if int(inp)

        tile, improvement = agent.getAction(simState)

        if tile is None:
            print("Turn {:3}: The Govenor does nothing this turn.".format(turn))
        else:
            print("Turn {:3}: The Govenor creates a new {} for the town.".format(turn, improvement.name))

        simState.update(tile, improvement)

        turn += 1

    printStatistics(simState)

# Call main fn when running this script (as opposed to importing it)
if __name__ == "__main__":
    main()