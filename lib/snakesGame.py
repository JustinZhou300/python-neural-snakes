import pygame
from enum import IntEnum
import random
from random import randint as rInt
from lib import Snake
import pickle

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class GameState(IntEnum):
    PLAY = 0
    PAUSE = 1
    RESET = -1 
    QUIT = -2
    SAVE = 2
    LOAD = 3

class saveGame:
    def __init__(self,snakes):
        self.snakes = snakes

class SnakeGame:

    class options:
        snakes = 1
        snakeEnergy = 250
        resolutionW = 800
        resolutionH = 600
        wBoundary = 30
        hBoundary = 30
        spawnRadius = 3
        tickRate = 30
        bodyLength = 3
        saveSnakes = "gameSave"

        def setOptions(self,var):
            for key, value in var.items():
                setattr(self,key,value)

    
    def __init__(self):
        self.snakes = self.options.snakes
        self.state = GameState.PLAY

    def drawSnake(self, snake, colour):
        head = pygame.Rect(snake.xPos*10, snake.yPos*10, 10, 10)
        pygame.draw.rect(self.screen, colour, head)
        for t in snake.body:
            pygame.draw.rect(self.screen, colour,
                             pygame.Rect(t[0]*10, t[1]*10, 10, 10))
        pygame.draw.rect(self.screen, colour, pygame.Rect(
            snake.applePosition[0]*10, snake.applePosition[1]*10, 10, 10))

    def displayText(self, text, x, y, fontSize = 14 ):
        largeText = pygame.font.Font('./PressStart2P-Regular.ttf', fontSize)
        TextSurf, TextRect = self.textObjects(text, largeText)
        TextRect.center = (x, y)
        self.screen.blit(TextSurf, TextRect)

    def drawBoundary(self):
        pygame.draw.rect(self.screen, RED, pygame.Rect(
            5, 5, SnakeGame.options.wBoundary*10, SnakeGame.options.hBoundary*10), 10)

    def textObjects(self, text, font):
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()

    def spawnSnakes(self, n):
        snakes = []
        centre = [int(SnakeGame.options.wBoundary/2 - 1), int(SnakeGame.options.hBoundary/2 - 1)]
        for i in range(0, n):
            random.seed(Snake.Snake.seed)
            temp = [rInt(centre[0]-self.options.spawnRadius, centre[0]+self.options.spawnRadius),
                    rInt(centre[1]-self.options.spawnRadius, centre[1]+self.options.spawnRadius)]
            snakes.append(Snake.Snake(temp[0], temp[1], WHITE,self.options.snakeEnergy,self.options.wBoundary,self.options.hBoundary,self.options.bodyLength))
        return snakes

    def gameInput(self, snake, n):  # to be overriden
        kbInput = snake.direction
        for event in self.events:  # User did something
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT):
                    kbInput = Snake.Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    kbInput = Snake.Direction.RIGHT
                if event.key == pygame.K_UP:
                    kbInput = Snake.Direction.UP
                if event.key == pygame.K_DOWN:
                    kbInput = Snake.Direction.DOWN

        return kbInput

    def gameOverLoop(self):
        while True:
            self.events = pygame.event.get()
            self.clock.tick(20)
            for event in self.events:  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.state = GameState.RESET
                        return 
                    if event.key == pygame.K_t:
                        self.state = GameState.RESET
                        random.seed()
                        Snake.Snake.appleSeed = rInt(1,10000)
                        return 
                    if event.key == pygame.K_l:
                        self.state = GameState.LOAD
                        return

    def snakeActions(self):
        i = 0  # index for snake
        snakesAlive = 0
        for snake in self.snakes:
            if snake.dead == False:
                snakesAlive += 1
                snake.senses()
                direction = self.gameInput(snake, i)
                snake.updateBody(direction)
                snake.move()
                snake.checkCollision()
                snake.getScore(self)
            i += 1
        if snakesAlive == 0:
            self.allDead = True

    def drawSnakes(self):
        i = 0
        x  = 1/2 * self.options.resolutionW 
        for snakeIndex, snake in enumerate(self.snakes):
            if snake.dead == False:
                self.drawSnake(snake, snake.colour)
            text = str("{0:.2f}".format(snake.score))      
            y =  15 + snakeIndex*self.options.resolutionH/10
            i += 1
            self.displayText(text,x,y) 
            text = " ".join(str("{0:.2f}".format(x)) for x in snake.collisionDistance + snake.decisionArray)
            self.displayText(text,3/5 * self.options.resolutionW,y+20) 
        self.drawExtra()

    def drawExtra(self): 
        return

    def userKeyInputs(self):
        self.events = pygame.event.get()
        for event in self.events:  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                self.state = GameState.QUIT
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state = GameState.RESET
                    return True
                if event.key == pygame.K_p:
                    if (self.state == GameState.PLAY):
                        self.state = GameState.PAUSE
                    else:
                        self.state = GameState.PLAY
                        return False
                if event.key == pygame.K_k:
                    self.state = GameState.SAVE
                    self.gameSave()
                if event.key == pygame.K_l:
                    self.state = GameState.LOAD
                    self.gameLoad()

        return False

    def gameSave(self):
        saveFile = open(fileName,'wb')
        save = saveGame(self.snakes)
        pickle.dump(save,saveFile,-1)
        saveFile.close()
        self.state = GameState.PLAY
        
    def gameLoad(self):
        saveFile = open(fileName,'rb')
        save = pickle.load(saveFile)
        self.snakes = save.snakes
        self.state = GameState.PLAY

    def gameLoop(self):
        done = False
        self.snakes = self.spawnSnakes(self.options.snakes)
        direction = 0
        self.allDead = False
        if self.state == GameState.LOAD:
            self.gameLoad()
        #self.t0 = time.time()
        while not done:
            self.clock.tick(self.options.tickRate)
            done = self.userKeyInputs()
            paused = (self.state == GameState.PAUSE)
            while paused:
                paused = self.pauseLoop()
            self.snakeActions()
            self.screen.fill(BLACK)
            self.drawBoundary()
            self.drawSnakes()
            if self.allDead == True:
                done = True
                self.gameOverLoop()
                return
            pygame.display.update()

    def pauseLoop(self):
        self.clock.tick(self.options.tickRate)
        self.userKeyInputs()
        return self.state == GameState.PAUSE

    def startLoop(self):
        self.clock.tick(self.options.tickRate)

    def startGame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.options.resolutionW, self.options.resolutionH))
        pygame.display.set_caption('Snakes')
        self.clock = pygame.time.Clock()
        while not self.state == GameState.QUIT:
            self.gameLoop()
        pygame.quit()

    def getAppleSeed(self):
        return Snake.Snake.appleSeed

    def randomiseAppleSeed(self):
        Snake.Snake.appleSeed = rInt(0,10000)
        
    


