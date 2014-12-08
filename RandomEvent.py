import random
import logging
import shared
import simulation

class Event:
        def __init__(self, message, messageOver, eventLength, effect, inverseEffect):
            self.message = message
            self.messageOver = messageOver
            self.eventLength = eventLength
            self.effect = effect
            self.inverseEffect = inverseEffect
            self.counter = 0
            self.fired = 0

        def eventOver(self):
            if self.counter >= self.eventLength:
                if self.messageOver: print(self.messageOver)
                if self.inverseEffect: self.inverseEffect()
                logging.debug("[Random Event - Over]")
                return True
            return False

        def handleEvent(self):
            if not self.fired:
                print(self.message)
                self.effect()
            self.fired = 1
            self.counter += 1

class RandomEvent:
    def __init__(self, simState):
        self.simState = simState
        self.activeEventList = []
        self.eventList = []
        self.randomEvents = [

        [
        "\nThe town has been smitten! And the frogs shall come up both on thee, and upon thy people, and upon all thy servants. - A random farm has been destroyed\n", 
        None, 1, lambda: self.tileTo(shared.tileState.Farm, shared.tileType.Both), lambda: None
        ],

        [
        "\nA mining company has gone bankrupt! Their mine has been abandoned.\n",
        None, 1, lambda: self.tileTo(shared.tileState.Mine, shared.tileType.Both), lambda: None
        ],

        [
        "\nThe town has been smitten! And upon their ponds, and upon all their pools of water, that they may become blood; and that there may be blood throughout all the land! - A farm has gone barren!\n",
        None, 1, lambda: self.tileTo(shared.tileState.Farm, shared.tileType.Baren), lambda: None
        ],

        [
        "\nExperimental crop research has produced excelent results in a farm! - Farming production rate has increased 150%!\n",
        None, 5, lambda: self.addFoodRateBuff(1.5), lambda: self.addFoodRateBuff(1)
        ],

        [
        "\nA mine has collapsed! - A random mine has gone baron\n",
        None, 1, lambda: self.tileTo(shared.tileState.Mine, shared.tileType.Baren), lambda: None
        ],

        [
        "\nA mine has struck gold! - Mining production rate has increased 150%!\n",
        None, 5, lambda: self.addProductionRateBuff(1.5), lambda: self.addProductionRateBuff(1)
        ]

        ]

    def addProductionFlatBuff(self, buff):
        self.simState.statusEffects[0] = buff

    def addFoodFlatBuff(self, buff):
        self.simState.statusEffects[1] = buff

    def addProductionRateBuff(self, buff):
        self.simState.statusEffects[2] = buff

    def addFoodRateBuff(self, buff):
        self.simState.statusEffects[3] = buff

    def tileTo(self, tileType, destState):
        # tileType = shared.tileState.Farm or shared.tileState.Mine
        tileList = []
        for pos, iterTile in self.simState.land.items(): 
            if iterTile.state is tileType:
                tileList.append(iterTile)
        if tileList:
            choice = random.choice(tileList)
            choice.state = None
            choice.type = destState

    def rateChange(self, tileType, rate):
        # tileType = shared.tileState.Farm or shared.tileState.Mine

        tileList = []
        for pos, iterTile in self.simState.land.items(): 
            if iterTile.state is tileType:
                tileList.append(iterTile)
        if tileList:
            choice = random.choice(tileList).tile 
            choice.productionRate *= rate
            choice.productionRate  = math.fabs(choice.productionRate)

    def killPeople(self, numberToKill):
        for x in range(numberToKill):
            self.simState.population.remove(random.choice(self.simState.population))

    def birthPeople(self, numberToBirth):
        for x in range(numberToBirth):
             self.simState.population.append(simulation.Person())

    def resetFoodHistory(self):
        self.simState.foodHistory = []

    def addEvents(self):
        for event in self.randomEvents:
            message, messageOver, eventLength, effect, inverseEffect = event
            temp = Event(message, messageOver, eventLength, effect, inverseEffect)
            self.eventList.append(temp)

    def rollRandomEvent(self):
        allowedEvents = []
        for x in self.eventList:
            if x in self.activeEventList: continue
            else: allowedEvents.append(x)
        # print("++allowedEvents+++", [i.message for i in allowedEvents])
        # print("++eventList+++", [i.message for i in self.eventList])
        # print("++activeEventList+++", [i self.activeEventList )
        if random.random() < .5 and len(allowedEvents) > 0: 
            self.activeEventList.append(random.choice(allowedEvents))
            logging.debug("[Random Event - Fired]")

    def playEvents(self):
        for event in self.activeEventList:
            if event.eventOver():
                if event in self.activeEventList: self.activeEventList.remove(event)
            event.handleEvent()
