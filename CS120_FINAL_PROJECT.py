# -*- coding: utf-8 -*-
"""
Created on Monday Nov 27 12:03:32 2023

@author: David Muana
"""

import pygame
import random

gameOverScreenActive = False
pygame.mixer.init()
pickedSound = pygame.mixer.Sound("PICKED.wav")
gruntSound = pygame.mixer.Sound("GRUNT.wav")

class Button:
    def __init__(self, text, position, size, color, hover_color, action=None):
        self.text = text
        self.position = position
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.rect = pygame.Rect(position, size)
        self.action = action

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class StartMenuScreen:
    def __init__(self, screen, backgroundImage):
        self.screen = screen
        self.backgroundImage = backgroundImage
        self.font = pygame.font.Font(None, 40)

        self.title_button = Button("2-Man Rumble", (225, 100), (200, 50), (255, 0, 0), (200, 0, 0))
        self.start_button = Button("Start", (250, 300), (150, 50), (0, 0, 255), (0, 0, 200), action=self.startGame)
        self.description_button = Button("Description", (250, 200), (150, 50), (0, 0, 255), (0, 0, 200), action=self.showDescription)
        self.quit_button = Button("Quit", (250, 400), (150, 50), (0, 0, 255), (0, 0, 200), action=pygame.quit)

        self.buttons = [self.title_button, self.description_button, self.start_button, self.quit_button]

        self.game_started = False

    def show_start_menu(self):
        pygame.mixer.music.load("MENU.mp3")
        pygame.mixer.music.play(-1)
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos) and not self.game_started:
                            if button.action:
                                button.action()
                                self.game_started = True
    
            self.screen.blit(self.backgroundImage, (0, 0))
    
            if not self.game_started:
                for button in self.buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.color = button.hover_color
                    else:
                        button.color = button.color
                    button.draw(self.screen, self.font)
    
                pygame.display.flip()
            else:
                pygame.mixer.music.stop()
                break
    
            if self.game_started:
               self.screen.blit(self.backgroundImage, (0, 0))
               pygame.display.flip()
               return

            if self.game_started:
                self.screen.blit(self.backgroundImage, (0, 0))
                pygame.display.flip()
                return

        self.description_button = Button("Description", (250, 200), (150, 50), (0, 0, 255), (0, 0, 200), action=self.showDescription)
       
    def startGame(self):
        startGame(self.screen, self.backgroundImage, coinGroup)

    def showDescription(self):
        description_screen = DescriptionScreen(self.screen, self.backgroundImage, self.show_start_menu)
        description_screen.show()
        
class DescriptionScreen:
    def __init__(self, screen, backgroundImage, back_callback):
        self.screen = screen
        self.backgroundImage = backgroundImage
        self.font = pygame.font.Font(None, 17)
        self.back_button = Button("Back", (250, 400), (150, 50), (0, 0, 255), (0, 0, 200), action=self.go_back)
        self.description_text = (
            "Red can be controlled by your arrow keys. Blue can be controlled by W A S D keys. Collect as much coins as you can. Get the boot for speed boost. Prevent one another from getting the coins by bumping into them"
        )
        self.back_callback = back_callback
    
    def go_back(self):
       self.back_callback()

    def show(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.rect.collidepoint(event.pos):
                        self.go_back()

            self.screen.blit(self.backgroundImage, (0, 0))

            top_half_text = self.description_text[:len(self.description_text) // 2]
            top_half_surface = self.font.render(top_half_text, True, (255, 255, 255))
            top_half_rect = top_half_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 20))
            self.screen.blit(top_half_surface, top_half_rect)

            bottom_half_text = self.description_text[len(self.description_text) // 2:]
            bottom_half_surface = self.font.render(bottom_half_text, True, (255, 255, 255))
            bottom_half_rect = bottom_half_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20))
            self.screen.blit(bottom_half_surface, bottom_half_rect)

            if self.back_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.back_button.color = self.back_button.hover_color
            else:
                self.back_button.color = self.back_button.color
            self.back_button.draw(self.screen, self.font)

            pygame.display.flip()

def showDescription(self):
    description_screen = DescriptionScreen(self.screen, self.backgroundImage)
    description_screen.show()

class Player:
    def __init__(self, image_path, initial_position, keys, speed=5):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = speed  
        self.keys = keys
        self.screen_width = 650
        self.screen_height = 480
        self.collected_coins = 0
        self.collected_chains = 0 
        self.chain_speed_boost = 2

    def move(self):
        keys = pygame.key.get_pressed()
        if self.collected_chains > 0:
            speed_with_boost = self.speed + self.chain_speed_boost
        else:
            speed_with_boost = self.speed

        new_rect = self.rect.copy()  

        if keys[self.keys[0]]:
            new_rect.y -= speed_with_boost
        if keys[self.keys[1]]:
            new_rect.y += speed_with_boost
        if keys[self.keys[2]]:
            new_rect.x -= speed_with_boost
        if keys[self.keys[3]]:
            new_rect.x += speed_with_boost

        player_bounding_box = pygame.Rect(0, 50, self.screen_width, self.screen_height - 50)

        if player_bounding_box.contains(new_rect):
            self.rect = new_rect

class Coin(pygame.sprite.Sprite):
    def __init__(self, image_path, screen_width, screen_height, score_rect=None):
        super().__init__()
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.score_rect = score_rect
        self.placeCoin()
        self.speed_x = 1  
        self.speed_y = 1  
    
    def update(self):
       self.rect.x += self.speed_x
       self.rect.y += self.speed_y

       if self.rect.x <= 0 or self.rect.x + self.rect.width >= self.screen_width:
           self.speed_x = -self.speed_x

       if self.rect.y <= 50 or self.rect.y + self.rect.height >= self.screen_height:
           self.speed_y = -self.speed_y
        
    def placeCoin(self):
        while True:
            self.rect.x = random.randint(0, self.screen_width - self.rect.width)
            self.rect.y = random.randint(50, self.screen_height - self.rect.height)

            if self.score_rect is None or not self.rect.colliderect(self.score_rect):
                break
            
    def collected(self):
        pickedSound.play()

class Chain(pygame.sprite.Sprite):
    def __init__(self, image_path, screen_width, screen_height, score_rect=None):
        super().__init__()
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.score_rect = score_rect
        self.placeCoin()
        self.speed_x = 1  
        self.speed_y = 1  
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x <= 0 or self.rect.x + self.rect.width >= self.screen_width:
            self.speed_x = -self.speed_x

        if self.rect.y <= 50 or self.rect.y + self.rect.height >= self.screen_height:
            self.speed_y = -self.speed_y

    def placeCoin(self):
        while True:
            self.rect.x = random.randint(0, self.screen_width - self.rect.width)
            self.rect.y = random.randint(50, self.screen_height - self.rect.height)
            
            if self.score_rect is None or not self.rect.colliderect(self.score_rect):
                break
            else:
                self.rect.y = max(50, self.rect.y)

class GameOverScreen:
    def __init__(self, screen, backgroundImage):
        self.screen = screen
        self.backgroundImage = backgroundImage
        self.font = pygame.font.Font(None, 40)

        self.restart_button = Button("Restart", (250, 200), (150, 50), (0, 0, 255), (0, 0, 200), action=self.restartGame)
        self.quit_button = Button("Quit", (250, 300), (150, 50), (0, 0, 255), (0, 0, 200), action=pygame.quit)
        self.buttons = [self.restart_button, self.quit_button]

    def restartGame(self):
        bluePlayer.collected_coins = 0
        bluePlayer.collected_chains = 0
        redPlayer.collected_coins = 0
        redPlayer.collected_chains = 0

        pygame.mixer.music.stop()

        coinGroup.empty()
        
        numChains = random.randint(1, 3)

        coinGroup.empty()
    
        for _ in range(20 - numChains):
            coin_type = "Coin1.PNG"
            coin = Coin(coin_type, 650, 480)
            coinGroup.add(coin)
    
        for _ in range(numChains):
            coin_type = "Chain.PNG"
            coin = Chain(coin_type, 650, 480)
            coinGroup.add(coin)

        startGame(self.screen, self.backgroundImage, coinGroup)

    
    def show(self):
        global gameOverScreenActive
        
        if not gameOverScreenActive:
            pygame.mixer.music.load("OVER.mp3")
            pygame.mixer.music.play(-1)
            gameOverScreenActive = True
            
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.action()
                            
            if not gameOverScreenActive:
                    break

            self.screen.blit(self.backgroundImage, (0, 0))

            winner_text = self.get_winner_text()

            game_over_text = self.font.render("Game Over!", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, 100))
            self.screen.blit(game_over_text, text_rect)

            # Draw winner or tie message
            winner_text_surface = self.font.render(winner_text, True, (255, 255, 255))
            winner_text_rect = winner_text_surface.get_rect(center=(self.screen.get_width() // 2, 150))
            self.screen.blit(winner_text_surface, winner_text_rect)

            for button in self.buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.color = button.hover_color
                else:
                    button.color = button.color
                button.draw(self.screen, self.font)

            pygame.display.flip()

    def get_winner_text(self):
        if bluePlayer.collected_coins > redPlayer.collected_coins:
            return "Blue Player Wins!"
        elif redPlayer.collected_coins > bluePlayer.collected_coins:
            return "Red Player Wins!"
        else:
            return "It's a Tie!"

coinGroup = pygame.sprite.Group()
bluePlayer = None 
redPlayer = None   

numChains = random.randint(1, 3)

for _ in range(20 - numChains):
    coin_type = "Coin1.PNG"
    coin = Coin(coin_type, 650, 480)
    coinGroup.add(coin)

for _ in range(numChains):
    coin_type = "Chain.PNG"
    coin = Chain(coin_type, 650, 480)
    coinGroup.add(coin)

def startGame(screen, backgroundImage, coinsGroup):
    global bluePlayer, redPlayer 

    print("Starting the game...")

    pygame.mixer.music.stop()

    pygame.mixer.music.load("GAME.WAV")
    pygame.mixer.music.play(-1)

    bluePlayer = Player("BLUE.png", (100, 100), (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d), speed=3)
    redPlayer = Player("RED.png", (500, 100), (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT), speed=3)

    blueCollectedCoins = 0
    redCollectedCoins = 0

    clock = pygame.time.Clock()
    timerFont = pygame.font.Font(None, 36)

    gameTimer = 300

    num_silver_coins = random.randint(1, 5)

    coinGroup.empty()

    for _ in range(20 - numChains):
        coin_type = "Coin1.PNG"
        coin = Coin(coin_type, 650, 480)
        coin.speed_x = random.choice([-1, 1])  
        coin.speed_y = random.choice([-1, 1])  
        coinGroup.add(coin)
    
    for _ in range(numChains):
        coin_type = "Chain.PNG"
        chain = Chain(coin_type, 650, 480)
        chain.speed_x = random.choice([-1, 1])  
        chain.speed_y = random.choice([-1, 1])  
        coinGroup.add(chain)

    for _ in range(num_silver_coins):
        coin_type = "SILVER.PNG"
        silver_coin = Coin(coin_type, 650, 480)
        coinGroup.add(silver_coin)

    for coin in coinsGroup:
        coin.placeCoin()

    while gameTimer > 0 and len(coinsGroup) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        bluePlayer.move()
        redPlayer.move()

        bluePlayer.rect.y = max(0, bluePlayer.rect.y)
        redPlayer.rect.y = max(0, redPlayer.rect.y)

        for coin in coinsGroup:
            coin.update()

        for coin in coinsGroup:
            coin.rect.y = max(50, coin.rect.y)
            
        for coin in pygame.sprite.spritecollide(bluePlayer, coinsGroup, True):
            if isinstance(coin, Chain):
                bluePlayer.collected_chains += 1
                bluePlayer.chain_speed_boost = 2
            elif coin.image_path == "SILVER.PNG":
                print("Blue collected SILVER coin!")
                bluePlayer.collected_coins += 2
                blueCollectedCoins += 2
                coin.collected() 
            else:
                bluePlayer.collected_coins += 1
                blueCollectedCoins += 1
                coin.collected()  
    
        for coin in pygame.sprite.spritecollide(redPlayer, coinsGroup, True):
            if isinstance(coin, Chain):
                redPlayer.collected_chains += 1
                redPlayer.chain_speed_boost = 2
            elif coin.image_path == "SILVER.PNG":  
                print("Red collected SILVER coin!")
                redPlayer.collected_coins += 2 
                redCollectedCoins += 2
                coin.collected()
            else:
                redPlayer.collected_coins += 1
                redCollectedCoins += 1
                coin.collected()

    
        if bluePlayer.rect.colliderect(redPlayer.rect):
            bounce_distance = 60
            if bluePlayer.rect.x < redPlayer.rect.x:
                bluePlayer.rect.x -= bounce_distance
                redPlayer.rect.x += bounce_distance
            else:
                bluePlayer.rect.x += bounce_distance
                redPlayer.rect.x -= bounce_distance
        
            if bluePlayer.rect.y < redPlayer.rect.y:
                bluePlayer.rect.y -= bounce_distance
                redPlayer.rect.y += bounce_distance
            else:
                bluePlayer.rect.y += bounce_distance
                redPlayer.rect.y -= bounce_distance
        
            gruntSound.play()
    
        screen.blit(backgroundImage, (0, 0))

        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(10, 7, 200, 30)) 
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 45, 200, 30)) 
    
        coinsGroup.draw(screen)
        coinsGroup.update()
    
        screen.blit(bluePlayer.image, bluePlayer.rect.topleft)
        screen.blit(redPlayer.image, redPlayer.rect.topleft)
    
        timerText = timerFont.render(f"Time: {gameTimer}", True, (255, 255, 255))
        screen.blit(timerText, (500, 20))
    
        font = pygame.font.Font(None, 36)
        blue_score_text = font.render(f"Blue Coins: {blueCollectedCoins}", True, (255, 255, 255))
        red_score_text = font.render(f"Red Coins: {redCollectedCoins}", True, (255, 255, 255))
        screen.blit(blue_score_text, (10, 10))
        screen.blit(red_score_text, (10, 50))
    
        pygame.display.flip()
        clock.tick(30)
    
        gameTimer -= 0.5
    
        if bluePlayer.collected_chains > 0:
            bluePlayer.chain_speed_boost -= 0.01
            if bluePlayer.chain_speed_boost < 0:
                bluePlayer.chain_speed_boost = 0
    
        if redPlayer.collected_chains > 0:
            redPlayer.chain_speed_boost -= 0.01
            if redPlayer.chain_speed_boost < 0:
                redPlayer.chain_speed_boost = 0
    
    print("Game over!")

    pygame.mixer.music.stop()

    game_over_screen = GameOverScreen(screen, backgroundImage)
    game_over_screen.show()
    
    game_over_screen = GameOverScreen(screen, backgroundImage)
    game_over_screen.show()

    return bluePlayer, redPlayer

def showStartMenu(screen, backgroundImage):
    font = pygame.font.Font(None, 40)

    screen.blit(backgroundImage, (0, 0))

    titleButton = Button("2-Man Rumble", (225, 100), (200, 50), (255, 0, 0), (200, 0, 0))
    startButton = Button("Start", (250, 300), (150, 50), (0, 0, 255), (0, 0, 200), action=lambda: startGame(screen, backgroundImage, coinGroup))
    descriptionButton = Button("Description", (250, 200), (150, 50), (0, 0, 255), (0, 0, 200), action=showDescription)
    quitButton = Button("Quit", (250, 400), (150, 50), (0, 0, 255), (0, 0, 200), action=pygame.quit)

    buttons = [titleButton, descriptionButton, startButton, quitButton]
    menuButtons = [titleButton, descriptionButton, startButton, quitButton]
    gameStarted = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos) and not gameStarted:
                        if button.action:
                            button.action()
                            gameStarted = True

        screen.blit(backgroundImage, (0, 0))

        if not gameStarted:
            for button in menuButtons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.color = button.hover_color
                else:
                    button.color = button.color
                button.draw(screen, font)

            pygame.display.flip()
        else:
            break

        if gameStarted:
            screen.blit(backgroundImage, (0, 0))
            pygame.display.flip()
            return

def main():
    pygame.init()
    screen = pygame.display.set_mode((650, 480))
    pygame.display.set_caption("2-man Rumble")

    backgroundImage = pygame.image.load("DarkB.PNG").convert()
    start_menu_screen = StartMenuScreen(screen, backgroundImage)
    start_menu_screen.show_start_menu()
    pygame.quit()

if __name__ == "__main__":
    main()
