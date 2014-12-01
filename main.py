#! /usr/bin/env python3

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
            print("Turn {}: No tile picked".format(turn))
        else:
            print("Turn {}: Agent upgrades {} by {}".format(turn, tile.state, improvement))

        simulationState.update(tile, improvement)
        turn += 1

# Call main fn when running this script (as opposed to importing it)
if __name__ == "__main__":
    main()