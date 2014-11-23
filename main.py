#! /usr/bin/env python3

from agent import *
from testsimulation import *

def main():
    # Generate a randomized starting simulation
    simulationState = SimulationState()
    agent = ReflexAgent()

    while True:
        # Break when theres no moves left for now
        if not simulationState.getPopulation():
            break

        tile, upgrade = agent.getAction(simulationState)

        simulationState.update(tile, upgrade)


# Call main fn when running this script (as opposed to importing it)
if __name__ == "__main__":
    main()