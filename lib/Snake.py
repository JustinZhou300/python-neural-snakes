import random
from random import randint as rInt
from enum import IntEnum
import math

class Direction(IntEnum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

NORMALISE = lambda x: 1/(0.01+x)

class Snake:
    seed = rInt(1, 10000)
    appleSeed =  rInt(1, 10000)
    maxEnergy = 100
    def __init__(self, xPos, yPos, colour, maxEnergy,wBoundary,hBoundary,bodyLength):
        self.xPos = xPos
        self.yPos = yPos
        random.seed(Snake.seed)
        i = rInt(1, 4)
        self.direction = i
        self.body = [] 
        self.createBody(bodyLength)
        self.applesEaten = 0
        self.colour = colour
        self.dead = False
        self.increaseLength = False
        #
        self.score = 0
        #
        self.decisionScore = 0
        self.sumDecisionScore = 0
        self.maxEnergy = maxEnergy
        self.energy = maxEnergy
        self.boundary = [wBoundary,hBoundary]
        #
        self.framesAlive = 0
        self.appleChangePosition()

    def createBody(self,bodyLength):  
        if self.direction == Direction.LEFT:
            [self.body.append( [self.xPos + bodyLength - i,self.yPos] ) for i in range(bodyLength)]
        elif self.direction == Direction.RIGHT:
            [self.body.append( [self.xPos - bodyLength + i,self.yPos] ) for i in range(bodyLength)]
        elif self.direction == Direction.UP:
            [self.body.append( [self.xPos,self.yPos + bodyLength - i] ) for i in range(bodyLength)]     
        elif self.direction == Direction.DOWN:
            [self.body.append( [self.xPos,self.yPos - bodyLength + i] ) for i in range(bodyLength)]     

    def updateBody(self, direction):
        self.body.append([self.xPos, self.yPos])
        if not self.increaseLength:
            del self.body[0]
        else:
            self.increaseLength = False
        if (direction == Direction.LEFT) and not (self.direction == Direction.RIGHT):
            self.direction = Direction.LEFT
        elif (direction == Direction.RIGHT) and not (self.direction == Direction.LEFT):
            self.direction = Direction.RIGHT
        elif (direction == Direction.UP) and not (self.direction == Direction.DOWN):
            self.direction = Direction.UP
        elif (direction == Direction.DOWN) and not (self.direction == Direction.UP):
            self.direction = Direction.DOWN

    def checkCollision(self):
       # out of bounds
        if (self.xPos <= 0 or self.xPos >= self.boundary[0] or self.yPos <= 0 or self.yPos >= self.boundary[1]):
            self.dead = True
            self.firstDeathFrame = True
        else:
            # check for self collision
            for t in self.body:
                if self.xPos == t[0] and self.yPos == t[1]:
                    self.dead = True
                    self.firstDeathFrame = True
                    break
        # check for apple collision
        if self.xPos == self.applePosition[0] and self.yPos == self.applePosition[1]:
            self.appleChangePosition()
            self.increaseLength = True
            self.applesEaten += 1
            self.energy = self.maxEnergy
        else:
            self.energy -= 1
            if self.energy <= 0:
                self.dead = True

    def senses(self):
        self.collisionDistance = [self.xPos, self.boundary[0] -self.xPos, self.yPos, self.boundary[1]-self.yPos]
        self.appleDistance = [1000,1000,1000,1000]
        self.appleDistance2 = [self.xPos-self.applePosition[0], self.yPos-self.applePosition[1]]
        #
        self.framesAlive += 1
        #
        if self.xPos-self.applePosition[0] >= 0:
            self.appleDistance[0]= self.xPos-self.applePosition[0] 
        else:
            self.appleDistance[1] = self.applePosition[0] - self.xPos
        
        if self.yPos-self.applePosition[1] >= 0:
            self.appleDistance[2] = self.yPos-self.applePosition[1]
        else:
            self.appleDistance[3] = self.applePosition[1] - self.yPos

        for block in self.body:
            if block[0] == self.xPos:
                distance = block[1] - self.yPos 
                if distance > 0 :
                    if distance < self.collisionDistance[2]:
                        self.collisionDistance[3] = distance
                else:
                    if abs(distance) < self.collisionDistance[3]:
                        self.collisionDistance[2] = abs(distance)
            elif block[1] == self.yPos:
                distance = block[0] - self.xPos
                if distance > 0:
                    if distance < self.collisionDistance[0]:
                        self.collisionDistance[1] = distance
                else: 
                    if abs(distance) < self.collisionDistance[1]:
                        self.collisionDistance[0] = abs(distance)
                    
            

        # for x in range(0, self.xPos):# from left wall to snake
        #     for block in self.body:
        #         if block == [x,self.yPos] :
        #             self.collisionDistance[0] = self.xPos - x

        # for x in range(self.boundary[0], self.xPos, -1):
        #     for block in self.body:
        #         if block == [x,self.yPos]:
        #             self.collisionDistance[1] = x - self.xPos

        # for y in range(0, self.yPos):
        #     for block in self.body:
        #         if block == [self.xPos,y]: 
        #             self.collisionDistance[2] = self.yPos - y

        # for y in range(self.boundary[1], self.yPos, -1):
        #     for block in self.body:
        #         if block == [self.xPos,y]:
        #             self.collisionDistance[3] = y - self.yPos

        self.collisionDistance = list(map(NORMALISE,self.collisionDistance))

        def getDecisionScore(self):
            self.decisionScore = -1          
            if self.appleDistance2[0] < 0:
                if self.direction == Direction.RIGHT:
                    self.decisionScore += 2
            elif self.appleDistance2[0] > 0:
                if self.direction == Direction.LEFT:
                    self.decisionScore += 2
            if self.appleDistance2[1] > 0:
                if self.direction == Direction.UP:
                    self.decisionScore += 2
            elif self.appleDistance2[1] < 0:
                if self.direction == Direction.DOWN:
                    self.decisionScore += 2

        def getDecisionArray(self):
            self.decisionArray = [0, 0, 0, 0]
            if self.appleDistance2 == [1, 0]:
                self.decisionArray[0] += 1
            elif self.appleDistance2 == [-1, 0]:
                self.decisionArray[1] += 1
            elif self.appleDistance2 == [0, 1]:
                self.decisionArray[2] += 1
            elif self.appleDistance2 == [0, -1]:
                self.decisionArray[3] += 1
            else:
                if self.appleDistance2[0] < 0:
                    self.decisionArray[1] += 1
                elif self.appleDistance2[0] > 0:
                    self.decisionArray[0] += 1
                if self.appleDistance2[1] > 0:
                    self.decisionArray[2] += 1
                elif self.appleDistance2[1] < 0:
                    self.decisionArray[3] += 1

        getDecisionScore(self)
        getDecisionArray(self)

    def move(self):
        if self.direction == Direction.LEFT:
            self.xPos -= 1
        elif self.direction == Direction.RIGHT:
            self.xPos += 1
        elif self.direction == Direction.UP:
            self.yPos -= 1
        elif self.direction == Direction.DOWN:
            self.yPos += 1

    def getScore(self, game):
        self.sumDecisionScore += self.decisionScore
        if self.sumDecisionScore < 0:
            self.sumDecisionScore = 0
        self.score = (self.framesAlive/100)**2 + ( self.sumDecisionScore/10 )**2 +  ( 2* (self.applesEaten) )**2

    def appleChangePosition(self):
        validPos = False
        while not validPos:
            validPos = True
            self.appleSeed += 1
            random.seed(self.appleSeed)
            self.applePosition = [rInt(1, self.boundary[0]-1), rInt(1, self.boundary[1]-1)]
            if (self.xPos == self.applePosition[0] and self.xPos == self.applePosition[1]):
                validPos = False
            else:
                for t in self.body:
                    if self.applePosition  == t:
                        validPos = False             
