# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    # must always initialize pygame
    pygame.init()

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # make the game screen and create a clock object for it
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0 #delta over time

    # groups to make the game easy to track, keep game loop logic simple
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    # update all game class containers to have appropriate groups
    Player.containers = (updateable, drawable)
    Asteroid.containers = (asteroids, updateable, drawable)
    AsteroidField.containers = (updateable)
    Shot.containers = (shots, updateable, drawable)

    # game objects, even if never directly accessed you must create the game objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # game loop
    while True:
        # is user quits the game, leave the game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        # tell the game clock to wait until 60fps
        clock.tick(60)
        # the amount of time since the last tick() call, in seconds
        dt = (clock.tick(60) / 1000)
        # all game logic should be done after filling the screen
        screen.fill("black")
        for draw in drawable:
            draw.draw(screen)
        updateable.update(dt)
        for asteroid in asteroids:
            if player.check_collision(asteroid):
                print("Game over!")
                return
            for shot in shots:
                if shot.check_collision(asteroid):
                    shot.kill()
                    asteroid.split()
        # update the screen, should always be last
        pygame.display.flip()

if __name__ == "__main__":
    main()