# TODO: Set a flag for being a 'nextGameState' that is checked in update() so random events dont apply
# TODO: Tweak foodHistory rewards and Person.isDead() dice roll
# TODO: Add random events

import shared
import random
import copy

map_width = 5
map_height = 5
maxAge = 100
startingPop = 10

class Tile:
    def __init__(self, position):
        # self.type = random.choice([t for t in shared.tileType])
        self.type = shared.tileType.Both
        self.state = None
        self.productionRate = random.randint(1, 3)
        self.position = position

class Person:
    def __init__(self):
        self.age = random.randint(1,90)
    def isDead():
        return random.randint(1,maxAge) < self.age

class SimulationState:
    def __init__(self):
        self.income = 0
        self.food = startingPop + 1
        self.foodHistory = 0
        self.population = [Person() for x in range(startingPop)]
        self.land = {(x, y):Tile((x,y)) for x in range(map_width) for y in range(map_height)}

    def getPossibleActions(self):
        # Return all of the unimproved tiles
        return [tile for key, tile in self.land.items() if tile.state is None]

    def update(self, tile, improvement):
        # AI chooses its move
        if tile is not None and improvement is not None:
            self.land[tile.position].state = improvement

        # Calculate profit
        for pos, iterTile in self.land.items():
            if iterTile.state is not None:
                self.income += iterTile.productionRate

        # Roll age-weighted dice to calculate remaning population
        for person in self.population:
            if person.isDead:
                if person in self.population: self.population.remove(person)
                print("He's dead Jim.")

        # Keep track of the preformance and reward food continual food surplus with a 'birth' , and continual deficit with a 'starvation'
        self.foodHistory = self.foodHistory + (self.food - len(self.population))
        print("Food for this turn is: " + str(self.food))
        print("Pop for this turn is: " + str(len(self.population)))
        print("Food History for this turn is: " + str(self.foodHistory))
        if self.foodHistory > 10:
            self.population.append(Person())
            print("A person was born")
        if self.foodHistory < -5: 
            self.population.pop(random.randrange(len(self.population)))
            print("A person has starved")

        # Random Event possible

        # Turn counter incremented? Either here or in main loop

    def nextGameState(self, tile, improvement):
        # TODO: Set a flag for being a 'nextGameState' that is checked in update() so random events dont apply
        nextState = copy.deepcopy(self)
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

    
