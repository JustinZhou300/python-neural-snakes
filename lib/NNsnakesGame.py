import pygame
from enum import IntEnum 
import random 
from random import randint as rInt
import numpy as np
import copy
from statistics import mean
import pickle
from lib import GeneticAlgorithm as GA
from lib import neuralNetwork as NN
from lib import snakesGame

class NeuralNets():
    def __init__(self):
        self.NNsnakes = []
    def createSnakeNN(self,population):
            for i in range(0,population):
                self.NNsnakes.append(NN.NeuralNet(8,4,2,6))
                self.NNsnakes[i].createNet()
            
class saveGame():
    def __init__(self,NeuralNets,snakesList,gen,round,scores,appleSeed):
        self.NeuralNets = NeuralNets
        self.gen = gen
        self.snakes = snakesList
        self.round = round
        self.scores = scores
        self.appleSeed = appleSeed

class NNSnakeGame(snakesGame.SnakeGame):

    class options(snakesGame.SnakeGame.options):
        generations = 10
        population = 0
        rounds = 5
        bestNNName = "bestNN"
        mutationRate = 0.02
        mutationRange = 1
        resetAppleSeedEachGen = True
        firstSelection = 5
        showScores = False

    def __init__(self):
        super().__init__()
        self.round = 0
        self.scores = []
        self.NeuralNets = NeuralNets()
        self.gen = 1

    def getRoundMaxScores(self):
        for snake in self.snakes:
            self.scores.append(snake.score)

    def startGame(self):
        self.population = self.options.rounds * self.options.snakes
        self.NeuralNets.createSnakeNN(self.population)
        super().startGame()

    def drawSnakes(self):
        x  = 3/5 * self.options.resolutionW
        for snakeIndex, snake in enumerate(self.snakes):
            if snake.dead == False:
                self.drawSnake(snake, snake.colour)
            y =  15 + snakeIndex*self.options.resolutionH/10
            if self.options.showScores == True:
                text = str("{0:.2f}".format(snake.score)) + " - " + " ".join(str("{0:.2f}".format(x)) for x in (snake.collisionDistance + snake.decisionArray) )
                self.displayText(text,x,y)               
        self.drawExtra()

    def gameSave(self):
        save = saveGame(self.NeuralNets,self.snakes,self.gen,self.round,self.scores, self.getAppleSeed() )
        saveFile = open(self.options.saveSnakes,'wb')
        pickle.dump(save,saveFile,-1)
        saveFile.close()
        self.state = snakesGame.GameState.PLAY

    def gameLoad(self):
        saveFile = open(self.options.saveSnakes,'rb')
        save = pickle.load(saveFile)
        self.NeuralNets = save.NeuralNets
        self.gen = save.gen
        self.round = save.round
        self.snakes = save.snakes
        self.scores = save.scores
        snakesGame.Snake.Snake.appleSeed = save.appleSeed
        self.state = snakesGame.GameState.PLAY
    
    def drawExtra(self):
        text = "gen: "+ str(self.gen) + " " + "group: " + str(self.round)
        self.displayText(text,1/5 * self.options.resolutionW,4/5 * self.options.resolutionH)
        if self.round > 1 :
            text = "Gen Stats - Top Score: "  + str("{0:.1f}".format(self.bestScore)) + " Mean : " + str(self.averageScore)
            self.displayText(text,3/5 * self.options.resolutionW,4/5 * self.options.resolutionH + 16)

    def gameOverLoop(self):
        self.round += 1
        self.getRoundMaxScores()
        scoresSortedIndex = np.argsort(self.scores)
        self.bestScore = self.scores[scoresSortedIndex[-1]]
        self.averageScore = mean(self.scores)
        if self.round < self.options.rounds:
            return True
        else: 
            if self.gen == self.options.generations:
                bestNeuralNet = self.NeuralNets.NNsnakes[scoresSortedIndex[-1]]
                fileObject = open(self.options.bestNNName,'wb')
                pickle.dump(bestNeuralNet,fileObject)
                self.state = snakesGame.GameState.QUIT
                return False
            for i in range(0,self.options.firstSelection):
                self.NeuralNets.NNsnakes[i] = self.NeuralNets.NNsnakes[scoresSortedIndex[-1-i]]
            for i in range(self.options.firstSelection,self.population):
                couple = GA.FitnessProportionateSelection(self.scores,2)
                child = GA.CrossOverFFNN( self.NeuralNets.NNsnakes[couple[0]], self.NeuralNets.NNsnakes[couple[1]],self.options.mutationRate,self.options.mutationRange ) 
                self.NeuralNets.NNsnakes[i] = child
            self.round = 0
            self.gen += 1
            self.scores.clear()
            self.averageScore = 0
            if self.options.resetAppleSeedEachGen:
                self.randomiseAppleSeed()
            return True

    def gameInput(self,snake,n):
        #Get neural net input
        NNinput = snake.collisionDistance + snake.decisionArray    
        NNinput = np.transpose( np.matrix(NNinput)).A
        outputs = self.NeuralNets.NNsnakes[n+self.round*self.options.snakes].updateNet(NNinput)
        indexNum = 0
        temp = 0
        for i in range(0,len(outputs)):#set highest output as snake
            if outputs[i][0] > temp:
                indexNum = i
                temp = outputs[i][0]
        return indexNum + 1
