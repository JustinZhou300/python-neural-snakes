from lib import NNsnakesGame

OPTIONS = {
    'snakes':20,
    'rounds':5,
    'generations':5,
    'mutationRate' :0.02,
    'mutationRange' :1,
    'resolutionW': 1200,
    'resolutionH': 600
}

game = NNsnakesGame.NNSnakeGame()
game.options.setOptions(game.options,OPTIONS)

game.startGame()


