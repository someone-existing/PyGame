# Import random for random numbers
import random

import threading
import time
# Import the pygame module
import pygame, sys
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import *

# Initialize pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.display.set_caption('Tinker Game')

move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
death_sound = pygame.mixer.Sound("Death.ogg")
power_sound = pygame.mixer.Sound("Power.ogg")

move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
death_sound.set_volume(0.5)
power_sound.set_volume(1)
font = pygame.font.SysFont("Comic Sans", 50)
gamefont = pygame.font.SysFont("Arial", 30)
boja = (0, 0, 0)
# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Variable to keep the main loop running
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

 
def main_menu():
    click = False
    while True:
 
        bg = pygame.image.load("bg.jpg")
        bg = pygame.transform.scale(bg, (800, 600))
        screen.blit(bg, (0,0))
        draw_text('Main Menu', font, (255, 255, 255), screen, 308, 20)
 
        mx, my = pygame.mouse.get_pos()

 
        button_1 = pygame.Rect(302, 102, 200, 50)
        button_2 = pygame.Rect(302, 202, 200, 50)
        outline_1 = pygame.Rect(300, 100, 205, 55)
        outline_2 = pygame.Rect(300, 200, 205, 55)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                quit()
        pygame.draw.rect(screen, (255, 255, 255), outline_1)
        pygame.draw.rect(screen, (255, 255, 255), outline_2)
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        draw_text('Play', font, (255, 255, 255), screen, 365, 110)
        draw_text('Quit', font, (255, 255, 255), screen, 365, 210)
 
 
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        clock.tick(60)
def quit():
    pygame.quit()
    sys.exit()
def game():
    start_ticks=pygame.time.get_ticks()
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load("jet.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            #self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect()

        def update(self, pressed_keys):
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -10) #move in place
                move_up_sound.play()
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 10)
                move_down_sound.play()
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-10, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(10, 0)

            # Keep player on the screen
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

    # Define the enemy object by extending pygame.sprite.Sprite
    # The surface you draw on the screen is now an attribute of 'enemy'
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            self.surf = pygame.image.load("missile.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            #self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
            self.speed = enemyspeed

        # Move the sprite based on speed
        # Remove the sprite when it passes the left edge of the screen
        def update(self):
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()          

    # Define the cloud object by extending pygame.sprite.Sprite
    # Use an image for a better-looking sprite
    class Cloud(pygame.sprite.Sprite):
        def __init__(self):
            super(Cloud, self).__init__()
            self.surf = pygame.image.load("cloud.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            # The starting position is randomly generated
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )

        # Move the cloud based on a constant speed
        # Remove the cloud when it passes the left edge of the screen
        def update(self):
            self.rect.move_ip(-5, 0)
            if self.rect.right < 0:
                self.kill()
    # Define the cloud object by extending pygame.sprite.Sprite
    # Use an image for a better-looking sprite
    class SuperPower(pygame.sprite.Sprite):
        def __init__(self):
            super(SuperPower, self).__init__()
            self.surf = pygame.image.load("power.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )

        # Move the sprite based on speed
        # Remove the sprite when it passes the left edge of the screen
        def update(self):
            self.rect.move_ip(-5, 0)
            if self.rect.right < 0:
                self.kill()
    # Create a custom event for adding a new enemy

    def superpowerdef():
        global superpowertimer
        superpowertimer = 0
        draw_text('SUPER POWER EXPIRED!!', gamefont, (255, 0, 0), screen, 40, 40)
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 165)

    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)

    ENEMYSPEED = pygame.USEREVENT + 3
    pygame.time.set_timer(ENEMYSPEED, 10000)

    SUPERPOWER = pygame.USEREVENT + 4
    pygame.time.set_timer(SUPERPOWER, random.randint(8500, 45000))

    # Instantiate player. Right now, this is just a rectangle.
    player = Player()

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    superpowers = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    enemyspeed = 8
    playerscore = 0
    global superpowertimer
    superpowertimer = 0
    running = True
    pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
    pygame.mixer.music.play(loops=-1)
    # Main loop
    while running:

        # Look at every event in the queue
        for event in pygame.event.get():
            print(event)
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    player.kill()
                    move_up_sound.stop()
                    move_down_sound.stop()
                    pygame.mixer.music.stop()
                    running = False
                    main_menu()

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                    player.kill()
                    move_up_sound.stop()
                    move_down_sound.stop()
                    pygame.mixer.music.stop()
                    running = False
                    main_menu()
            # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                #Setting enemy speed after every 10 seconds, and player score every 10 seconds
            elif event.type == ENEMYSPEED:
                enemyspeed += random.randint(0, 7)
                playerscore += 1
            # Add a new cloud?
            elif event.type == ADDCLOUD:
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
            elif event.type == SUPERPOWER:
                new_power = SuperPower()
                superpowers.add(new_power)
                all_sprites.add(new_power)
            # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()
        # Update the player sprite based on user keypresses
        player.update(pressed_keys)
        enemies.update()
        clouds.update()
        superpowers.update()
        # Fill the screen with sky blue
        screen.fill((135, 206, 250))
        # Draw surf at the new coordinates
        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        seconds = 0
        seconds += (pygame.time.get_ticks()-start_ticks)/1000
        timer = 'Timer: ' + str(seconds)
        screen.blit(gamefont.render(timer, True, boja), (20, 5))
        score = 'Score: ' + str(playerscore)
        screen.blit(gamefont.render(score, True, boja), (20, 45))
        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, superpowers):
            superpowertimer = 1
            new_power.kill()
            power_sound.play()
            t = threading.Timer(5.0, superpowerdef)
            t.start()
        if superpowertimer == 1:
            draw_text('Super power expiring in 5 seconds!!', gamefont, (255, 0, 0), screen, 20, 85)
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            if superpowertimer == 0:
                death_sound.play()
                player.kill()

                move_up_sound.stop()
                move_down_sound.stop()
                pygame.mixer.music.stop()
                print("Time alive", seconds, "seconds")
                print("Your score was", playerscore, "!")
                # collChannel = collision_sound.play()
                
                running = False
                main_menu()

            
        pygame.display.update()
        # Ensure program maintains a rate of 30 frames per second
        clock.tick(60)
    # while collChannel.get_busy():
    #     pygame.time.wait(100)

    # All done! Stop and quit the mixer.
main_menu()
