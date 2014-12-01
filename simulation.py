# TODO: Set a flag for being a 'nextGameState' that is checked in update() so random events dont apply
# TODO: Tweak foodHistory rewards and Person.isDead() dice roll
# TODO: Add random events

import shared
import random
import logging
import copy

#### Game Defines ####
map_width = 5
map_height = 5
maxAge = 100
startingPop = 10

class Tile:
    def __init__(self, position):
        self.type = random.choice([t for t in shared.tileType])
        self.state = None
        self.productionRate = random.randint(1, 3)
        self.position = position

class Person:
    def __init__(self):
        self.age = random.randint(1,90)

    def ageByYear(self, year):
        self.age += year

    def getAge(self):
        return self.age

    def chanceToDie(self):
        #Calculate area under x^2+2/3 from 0 to self.age/100
        #Note: Might be too aggressive, idea is that chanceToDie at age 100 is 1
        age = self.age/100
        chanceToDie = (age ** 3)/3 + (2 * age)/3
        return chanceToDie

    def isDead(self):
        diceRoll = random.random()
        if diceRoll <= self.chanceToDie():
            logging.debug("[Population - Death] Age: " + str(self.getAge()) + " Chance to die: " + str(self.chanceToDie()) + " Dice Roll: " + str(diceRoll))  
            return True
        return False

class SimulationState:
    def __init__(self):
        self.income = 0
        self.food = startingPop + 1
        self.foodHistory = []
        self.population = [Person() for x in range(startingPop)]
        self.land = {(x, y):Tile((x,y)) for x in range(map_width) for y in range(map_height)}
        #simFlag is a flag for avoiding random event rolls durning a call to nextGameState() -- 0 = real state 1 = simulation state
        self.simFlag = 0

    def getPossibleActions(self):
        # Return all of the unimproved tiles
        return [tile for key, tile in self.land.items() if tile.state is None]

    def calculateFoodHistory(self):
        # Keep a FILO queue of the delta food of the last 10 moves
        if len(self.foodHistory) >= 10:
            self.foodHistory.pop()
        self.foodHistory.append(self.food - len(self.population))

    def calculateOutput(self):
        # Calculate profit and food this turn
        for pos, iterTile in self.land.items():
            if iterTile.state is shared.tileState.Mine:
                self.income += iterTile.productionRate
                logger.info("[Income - Value] this turn: " + str(self.income))
            if iterTile.state is shared.tileState.Farm:
                self.food += iterTile.productionRate
                logger.info("[Food - Value] this turn: " + str(self.food))

    def update(self, tile, improvement):
        # AI chooses its move
        if tile is not None and improvement is not None:
            self.land[tile.position].state = improvement

        self.calculateOutput()

        # Roll age-weighted dice to calculate remaning population
        for person in self.population:
            person.ageByYear(1)
            if person.isDead():
                if person in self.population: self.population.remove(person)

        # Calculate food history now that population has settled this turn
        self.calculateFoodHistory()

        # Reward continual food surplus with a 'birth', and continual deficit with a 'starvation'
        logging.debug("[Food - Value] this turn: " + str(self.food))
        logging.debug("[Population - Value] this turn: " + str(len(self.population))) 
        logging.debug("[Food - Net] this turn: " + str(self.food - len(self.population))) 
        logging.debug("[Food History - Value] this turn is: " + str(self.getFoodHistory()))
        if self.getFoodHistory() > 10:
            self.population.append(Person())
            logging.info("[Population - Birth] Due to foodHistory > 10")
        if self.getFoodHistory() < -5: 
            self.population.pop(random.randrange(len(self.population)))
            logging.info("[Population - Death] Due to foodHistory < -5")

        # Random Event possible

        # Turn counter incremented? Either here or in main loop

    def nextGameState(self, tile, improvement):
        # TODO: Set a flag for being a 'nextGameState' that is checked in update() so random events dont apply
        nextState = copy.deepcopy(self)
        nextState.simFlag = 1
        nextState.land[tile.position].state = improvement
        return nextState 
        # Testing
        # print("Call to nextGameState() updated tile: " + str(tile.position)  + " with improvement " + str(improvement))
        # print("Corresponding state at: " + str(self.land[tile.position].position) + " has improvement " + str(self.land[tile.position].state))


    def stillAlive(self):
        return len(self.population) > 0 # and other condition

    # Getters
    
    def getCurrentScore(self):
        return self.income + self.population

    def getIncome(self):
        return self.income

    def getFood(self):
        return self.food

    def getPopulation(self):
        return self.population

    def getLand(self):
        return self.land

    def getFoodHistory(self):
        return sum(self.foodHistory)
    
