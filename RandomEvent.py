import random
import logging
import shared

class Event:
        def __init__(self, message, messageOver, eventLength, effect, inverseEffect):
            self.message = message
            self.messageOver = messageOver
            self.eventLength = eventLength
            self.effect = effect
            self.inverseEffect = inverseEffect
            self.counter = 0

        def eventOver(self):
            if self.counter >= self.eventLength:
                if self.messageOver: print(self.messageOver)
                if self.inverseEffect: self.inverseEffect()
                logging.debug("[Random Event - Over]")
                return True
            return False

        def handleEvent(self):
            logging.info(self.message)
            self.effect()
            self.counter += 1

class RandomEvent:
    def __init__(self, simState):
        self.simState = simState
        self.activeEventList = []
        self.eventList = []
        self.randomEvents = [

        ["plague on", "plague off", 1, lambda: self.addFoodFlatBuff(100), lambda: self.addFoodFlatBuff(-100)]

        ]

    def addProductionFlatBuff(self, buff):
        self.simState.statusEffects[0] += buff

    def addFoodFlatBuff(self, buff):
        self.simState.statusEffects[1] += buff

    def addProductionRateBuff(self, buff):
        self.simState.statusEffects[2] += buff

    def addFoodRateBuff(self, buff):
        self.simState.statusEffects[3] += buff

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
        if random.random() < .5 and len(allowedEvents) > 0: 
        # if len(allowedEvents) >  0:
            self.activeEventList.append(random.choice(allowedEvents))
            logging.debug("[Random Event - Fired]")

    def playEvents(self):
        for event in self.activeEventList:
            if event.eventOver():
                if event in self.activeEventList: self.activeEventList.remove(event)
            event.handleEvent()
