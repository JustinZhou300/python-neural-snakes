from lib import snakesGame
OPTIONS = {
    'resolutionW': 1000,
    'resolutionH': 600,
    'bodyLength':10
}

game = snakesGame.SnakeGame()
game.options.setOptions(game.options,OPTIONS)
game.startGame()