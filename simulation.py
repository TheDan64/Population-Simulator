import shared
import random
import logging
import copy
import math
import RandomEvent

class Tile:
    def __init__(self, position):
        self.type = random.choice([t for t in shared.tileType])
        self.state = None
        self.productionRate = random.randint(1, 3)
        self.position = position

class Person:
    def __init__(self):
        self.age = random.randint(1,35)

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
    def __init__(self, map_width, map_height, maxAge, startingPop, quiet):
        self.map_width = map_width
        self.map_height = map_height
        self.maxAge = maxAge
        self.startingPop = startingPop
        self.income = 0
        self.food = startingPop + 1
        self.foodHistory = []
        self.population = [Person() for x in range(self.startingPop)]
        self.land = {(x, y):Tile((x,y)) for x in range(self.map_width) for y in range(self.map_height)}
        # simFlag is a flag for avoiding random event rolls durning a call to nextGameState() -- 0 = real state 1 = simulation state
        self.simFlag = 0
        self.turn = 0
        self.quiet = quiet
        # productionFlatBuff, foodFlatBuff, productionRateBuff, foodRateBuff 
        self.statusEffects = [0,0,1,1]
        self.randomEvent = RandomEvent.RandomEvent(self)
        self.randomEvent.addEvents()
        self.incomeThisTurn = 0
        self.foodThisTurn = 0

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
        self.incomeThisTurn = 0
        self.foodThisTurn = 0

        for pos, iterTile in self.land.items():
            if iterTile.state is shared.tileState.Mine:
                self.incomeThisTurn += iterTile.productionRate
            if iterTile.state is shared.tileState.Farm:
                self.foodThisTurn += iterTile.productionRate

        if not self.simFlag:
            logging.debug("[Random Events - Real State] In the real state, updating with status effects.")
            self.income += (self.incomeThisTurn + self.statusEffects[0]) * self.statusEffects[2]
            self.food += (self.foodThisTurn + self.statusEffects[1]) * self.statusEffects[3]
        else:
            logging.debug("[Random Events - Simulation State] In a simulation state, status effects do not apply.")
            self.income += self.incomeThisTurn
            self.food += self.foodThisTurn

        logging.info("[Income - Value] this turn: " + str(self.income))
        logging.info("[Food - Value] this turn: " + str(self.food))

    def update(self, tile, improvement):
        # AI chooses its move
        if tile is not None and improvement is not None:
            self.land[tile.position].state = improvement

        if not self.simFlag:     
            self.randomEvent.rollRandomEvent()
            self.randomEvent.playEvents()

        # Roll age-weighted dice to calculate remaning population
        for person in self.population:
            person.ageByYear(1)
            if person.isDead():
                if person in self.population: self.population.remove(person)

        self.calculateOutput()

        # Calculate food history now that population has settled this turn
        self.calculateFoodHistory()

        # Reward continual food surplus with a 'birth', and continual deficit with a 'starvation'
        logging.debug("[Food - Net] this turn: " + str(self.food - len(self.population))) 
        logging.debug("[Food History - Value] this turn is: " + str(self.getFoodHistory()))
        logging.debug("[Population - Value] this turn: " + str(len(self.population))) 
        if self.getFoodHistory() > 10:
            for i in range( math.floor(self.getFoodHistory() % 10) ):
                self.population.append(Person())
                logging.debug("[Population - Birth] Due to foodHistory > 10")
        if self.getFoodHistory() < -5: 
            self.population.pop(random.randrange(len(self.population)))
            logging.info("[Population - Death] Due to foodHistory < -5")

        self.turn += 1

    def nextGameState(self, tile, improvement):
        nextState = copy.deepcopy(self)
        nextState.simFlag = 1
        nextState.update(tile, improvement)
        return nextState 

    def stillAlive(self):
        # This was a triumph
        return len(self.population) > 0 

    # Getters
    
    def getCurrentScore(self):
        if len(self.population) ==  0:
            return 0
        
        # The heuristic that conbines elements of the other two
        if shared.heuristic == 1:
            return self.income / (len(self.population)*(self.getFoodHistory())) # Worst

        # Our 2nd idea heuristic
        elif shared.heuristic == 2:
            return self.income / len(self.population)

        # Our original heuristic
        return self.income * .1 + len(self.population) * (self.getFoodHistory()) # Best

    def getIncome(self):
        return self.income

    def getFood(self):
        return self.food

    def getPopulation(self):
        return self.population

    def getLand(self):
        return self.land

    def getFoodHistory(self):
        if len(self.foodHistory) == 0:
            return 1
        if sum(self.foodHistory)/(len(self.foodHistory) + 1) == 0:
            return 1
        return sum(self.foodHistory)/(len(self.foodHistory) + 1)
    
    def getTurn(self):
        return self.turn

    def getQuiet(self):
        return self.quiet
