import shared
import random
import logging
import copy
import RandomEvent

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
        # simFlag is a flag for avoiding random event rolls durning a call to nextGameState() -- 0 = real state 1 = simulation state
        self.simFlag = 0
        self.turn = 0
        # productionFlatBuff, foodFlatBuff, productionRateBuff, foodRateBuff 
        self.statusEffects = [0,0,1,1]
        self.randomEvent = RandomEvent.RandomEvent(self)
        self.randomEvent.addEvents()

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
            if iterTile.state is shared.tileState.Farm:
                self.food += iterTile.productionRate

        if not self.simFlag:
            logging.debug("[Random Events - Real State] In the real state, updating with status effects.")
            self.income = (self.income + self.statusEffects[0]) * self.statusEffects[2]
            self.food = (self.food + self.statusEffects[1]) * self.statusEffects[3]
        else:
            logging.debug("[Random Events - Simulation State] In a simulation state, status effects do not apply.")

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
            self.population.append(Person())
            logging.info("[Population - Birth] Due to foodHistory > 10")
        if self.getFoodHistory() < -5: 
            self.population.pop(random.randrange(len(self.population)))
            logging.info("[Population - Death] Due to foodHistory < -5")

        self.turn += 1

    def nextGameState(self, tile, improvement):
        # TODO: Set a flag for being a 'nextGameState' that is checked in update() so random events dont apply
        nextState = copy.deepcopy(self)
        nextState.simFlag = 1
        nextState.update(tile, improvement)
        return nextState 
        # Testing


    def stillAlive(self):
        return len(self.population) > 0 # and other condition

    # Getters
    
    def getCurrentScore(self):
        return self.income + len(self.population)   

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
    
