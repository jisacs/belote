"""
main module
"""
import pygame


cardBack = pygame.image.load('images/BACK.png')
cardBack = pygame.transform.scale(cardBack, (int(238*0.8), int(332*0.8)))


def renderGame(window):
    window.fill((15, 0, 169))
    font = pygame.font.SysFont("comicsans", 60, True)

    window.blit(cardBack, (100, 200))
    window.blit(cardBack, (700, 200))

    text = font.render(
        str(len(gameEngine.player1.hand)) + " cards", True, (255, 255, 255)
    )
    window.blit(text, (100, 500))

    text = font.render(
        str(len(gameEngine.player2.hand)) + " cards", True, (255, 255, 255)
    )
    window.blit(text, (700, 500))

    topCard = gameEngine.pile.peek()
    if topCard != None:
        window.blit(topCard.image, (400, 200))

    if gameEngine.state == GameState.PLAYING:
        text = font.render(
            gameEngine.currentPlayer.name + " to flip", True, (255, 255, 255)
        )
        window.blit(text, (20, 50))

    if gameEngine.state == GameState.SNAPPING:
        result = gameEngine.result
        if result["isSnap"] == True:
            message = "Winning Snap! by " + result["winner"].name
        else:
            message = (
                "False Snap! by "
                + result["snapCaller"].name
                + ". "
                + result["winner"].name
                + " wins!"
            )
        text = font.render(message, True, (255, 255, 255))
        window.blit(text, (20, 50))

    if gameEngine.state == GameState.ENDED:
        result = gameEngine.result
        message = "Game Over! " + result["winner"].name + " wins!"
        text = font.render(message, True, (255, 255, 255))
        window.blit(text, (20, 50))





if __name__ == "__main__":
    pygame.init()
    bounds = (1024, 768)
    window = pygame.display.set_mode(bounds)
    pygame.display.set_caption("SnaPy")
    """    
    We've built the model and the logic in the engine to play a game of Snap. Now we need to define the game loop to run the game.
    Open up the main.py file again. We'll start by adding references to the models and engine, so that we can access them when building the UI. Add the following imports right under the import pygame line:
    """
    from models import *
    from engine import *

    """
    We'll start by creating a new game engine object. Add this to the main.py file, underneath the Pygame initialization code:
    """
    gameEngine = SnapEngine()
    """
    Now the game loop. The game loop's job is to listen for user input, call the engine's play method to process that input, and update the UI with the result. Add this to the main.py file:
    """
    run = True
    while run:
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                key = event.key

        gameEngine.play(key)
        renderGame(window)
        pygame.display.update()

        if gameEngine.state == GameState.SNAPPING:
            pygame.time.delay(3000)
            gameEngine.state = GameState.PLAYING

    cardBack = pygame.image.load("images/BACK.png")
    cardBack = pygame.transform.scale(cardBack, (int(238 * 0.8), int(332 * 0.8)))
