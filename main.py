#! /usr/bin/env python3

"""
    This file contains the main loop to get the Agent and Environment working
    together. Also takes care of user input to pause or proceed with the
    simulation.
"""

from agent import *
from simulation import *
import argparse

parser = argparse.ArgumentParser(description="A population simulation")
parser.add_argument("--width", type=int, default=5, help="Width of the simulation grid (default: 5)")
parser.add_argument("--height", type=int, default=5, help="Height of the simulation grid (default: 5)")
parser.add_argument("--population", type=int, default=10, help="Starting population of the town (default: 10)")
parser.add_argument("--turns", type=int, default=25, help="Maximum number of turns (default: 25)")
parser.add_argument("--heuristic", type=int, default=1, help="Which heuristic to use 1 - 3 (default: 1)")
parser.add_argument("--quiet", type=int, default=0, help="Supress run output and run --turns times, outputting an average score over --turns runs")
parser.add_argument("--file", default="output", help="Output file name (defualt: 'output')")



args = parser.parse_args()

shared.heuristic = args.heuristic

def printStatistics(population, food, income, total, f='f'):
    if args.quiet:
        f.write("""Town Statistics
        Population:  {}
        Food:        {}
        Income:      {}
        Total:       {}\n
    """.format(population, food, income, total))
    else:
        print("""Town Statistics
        Population:  {}
        Food:        {}
        Income:      {}
        Total:       {}\
    """.format(population, food, income, total))

def main():
    # Generate a randomized starting simulation
     
    if args.quiet:
        totalPop = 0
        totalFood = 0
        totalIncome = 0
        totalScore = 0

        f = open(args.file, 'w+')
        f.write("stuff")
        for x in range(args.turns):
            f.write("Running heuristic " + str(heuristic) + " on iteration " + str(x) + "\n")
            simState = SimulationState(args.width, args.height, 100, args.population)
            simState.quiet = 1
            agent = ReflexAgent()
            while simState.stillAlive() and simState.getTurn() <= args.turns:
                tile, improvement = agent.getAction(simState)
                simState.update(tile, improvement)
            totalPop += len(simState.getPopulation())
            totalFood += simState.getFood()
            totalIncome += simState.getIncome()
            totalScore += simState.getFood() + len(simState.getPopulation()) + simState.getIncome()
        printStatistics(totalPop/args.turns, totalFood/args.turns, totalIncome/args.turns, totalScore/args.turns, f)
        f.close()
    else:
        simState = SimulationState(args.width, args.height, 100, args.population)
        agent = ReflexAgent()
        skipInputTurns = 0

        # End when theres no moves left or population is dead
        while simState.stillAlive() and simState.getTurn() <= args.turns:
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
                        printStatistics(len(simState.getPopulation()), simState.getFood(), simState.getIncome(), (simState.getFood() + len(simState.getPopulation()) + simState.getIncome()) ) 

            tile, improvement = agent.getAction(simState)

            if tile is None:
                print("Turn {:3}: The Govenor does nothing this turn.".format(simState.getTurn()))
            else:
                text = "\033[92mFarm\033[0m"

                if improvement.name == "Mine":
                    text = "\033[31;40mMine\033[0m"

                print("Turn {:3}: The Govenor creates a new {} for the town.".format(simState.getTurn(), text))

            simState.update(tile, improvement)

            if skipInputTurns > 0:
                skipInputTurns -= 1

        printStatistics(len(simState.getPopulation()), simState.getFood(), simState.getIncome(), (simState.getFood() + len(simState.getPopulation()) + simState.getIncome()))

# Call main fn when running this script (as opposed to importing it)
if __name__ == "__main__":
    main()