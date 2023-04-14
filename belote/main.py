"""
main module
"""
import pygame


from belote_engine import *

cardBack = pygame.image.load("images/BACK.png")
cardBack = pygame.transform.scale(cardBack, (int(238 * 0.8), int(332 * 0.8)))


if __name__ == "__main__":
    pygame.init()
    bounds = (2044, 1536)
    window = pygame.display.set_mode(bounds)
    pygame.display.set_caption("SnaPy")
    """    
    We've built the model and the logic in the engine to play a game of Snap. Now we need to define the game loop to run the game.
    Open up the main.py file again. We'll start by adding references to the models and engine, so that we can access them when building the UI. Add the following imports right under the import pygame line:
    """

    """
    We'll start by creating a new game engine object. Add this to the main.py file, underneath the Pygame initialization code:
    """
    gameEngine = BeleteEngine()
    """
    Now the game loop. The game loop's job is to listen for user input, call the engine's play method to process that input, and update the UI with the result. Add this to the main.py file:
    """

    def renderGame(window):
        # window.fill((15, 0, 169))
        font = pygame.font.SysFont("comicsans", 60, True)

        """
        window.blit(cardBack, (50, 250))
        window.blit(cardBack, (700, 250))
        window.blit(cardBack, (350, 50))
        window.blit(cardBack, (350, 450))
        """
        black = (255, 255, 255)
        selected_color = (255, 0, 0)

        for player in gameEngine.players:
            color = black
            if gameEngine.currentPlayer == player:
                color = selected_color
            text = font.render(player.name, True, color)
            window.blit(text, (player.position.x, player.position.y + 50))
        """
        text = font.render(
            gameEngine.player1.name,  True, (255, 255, 255)
        )
        window.blit(text, (gameEngine.player1.position.x, gameEngine.player1.position.y+50))

        text = font.render(
            gameEngine.player2.name, True, (255, 255, 255)
        )
        window.blit(text, (gameEngine.player2.position.x, gameEngine.player2.position.y+50))

        text = font.render(
            gameEngine.player3.name, True, (255, 255, 255)
        )
        window.blit(text, (gameEngine.player3.position.x, gameEngine.player3.position.y+50))

        text = font.render(
            gameEngine.player4.name, True, (255, 255, 255)
        )
        window.blit(text, (gameEngine.player4.position.x, gameEngine.player4.position.y+50))
        """
        """
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
        """

    for player in gameEngine.players:
        for card in player.hand:
            window.blit(card.image, (card.pos.x, card.pos.y))

    run = True
    while run:
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                key = event.key
                print(key)

        gameEngine.play(key)
        renderGame(window)
        pygame.display.update()

        """
        if gameEngine.state == GameState.SNAPPING:
            pygame.time.delay(3000)
            gameEngine.state = GameState.PLAYING
        """
    """    
    cardBack = pygame.image.load("images/BACK.png")
    cardBack = pygame.transform.scale(cardBack, (int(238 * 0.8), int(332 * 0.8)))
    """
