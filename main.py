#! /usr/bin/env python3

from agent import *
from testsimulation import *

def main():
	# Generate a randomized starting simulation
	simulationState = SimulationState()
	agent = ReflexAgent()

	while True:
		move = agent.getMove(simulationState)

		simulationState.update(move)

		break # tmp

# Call main fn when running this script (as opposed to importing it)
if __name__ == "__main__":
	main()