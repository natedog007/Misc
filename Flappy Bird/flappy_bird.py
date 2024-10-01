# Nathan Boyden
# This is my second python project creating flappy bird and then creating an AI to beat flappy bird

# The following imports are the libraries needed for the project

import pygame
import neat
import time
import os
import random

pygame.font.init()

# Constant values for game window resolution 600x800
WIN_WIDTH = 500
WIN_HEIGHT = 800

GEN = 0

# Using pygame's functions to set, scale, load, and join pngs to in-game sprites
BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Fonts for scoreboard
STAT_FONT = pygame.font.SysFont("", 50)


# This is the bird class that defines all aspects of the bird in-game and will be called upon later with the AI's
class Bird:
    IMAGES = BIRD_IMAGES
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    # A function that defines default values for things like position, speed, and frame count
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.images_count = 0
        self.image = self.IMAGES[0]

    # A jump function for editing jump characteristics
    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    # A function to define the actual movement of the jump -10.5 + 1.5 = 9,7,5,3,1,... changes position based on the
    # time elapsed and the velocity which at the point of the jump is -10.5
    def move(self):
        self.tick_count += 1
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        # This sets terminal velocity downward
        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement -= 2

        # This applies the change to the height of the bird
        self.y = self.y + displacement

        # If the bird is falling past the center of the screen the rotation of the bird will then
        # match its direction
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    # This plays a frame of the bird sprite after a specific amount of
    # time after all 4 sprites are shown the image_count variable is restarted and
    # The first image is displayed
    def draw(self, win):

        self.images_count += 1

        if self.images_count < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]

        elif self.images_count < self.ANIMATION_TIME * 2:
            self.image = self.IMAGES[1]

        elif self.images_count < self.ANIMATION_TIME * 3:
            self.image = self.IMAGES[2]

        elif self.images_count < self.ANIMATION_TIME * 4:
            self.image = self.IMAGES[1]

        elif self.images_count == self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMAGES[0]
            self.images_count = 0

        # This one is specifically for when the bird tilts downward
        # Setting the sprite to the wing down position and adjusting the time as well
        if self.tilt <= -80:
            self.image = self.IMAGES[1]
            self.images_count = self.ANIMATION_TIME * 2

        # Rotates sprite
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


# This is the pipe class that defines all aspects of the pipes in-game will collision
class Pipe:
    GAP = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        # Having normal texture for bottom pipe and a flipped for the top
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE

        # Collision variable between bird and pipe
        self.passed = False

        self.set_height()

    def set_height(self):
        # Random height
        self.height = random.randrange(50, 450)
        # Height of the pipe minus the random pixel count found above is where the texture starts
        self.top = self.height - self.PIPE_TOP.get_height()
        # Just sets the bottom pipe to be at a random height plus (or negative because the y-axis is flipped) a
        # predetermined gap
        self.bottom = self.height + self.GAP

    def move(self):
        # moves the sprite to the left by the unit VELOCITY defined earlier
        self.x -= self.VELOCITY

    def draw(self, win):
        # Draws top pipe
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # Draws bottom pipe
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        # Sets masks
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # IDK
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Checking if pixels overlap and if they collide they will return a value, if not they return NONE
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        # If either point returns anything make collision True
        if t_point or b_point:
            return True

        return False


class Base:
    VELOCITY = 5
    WIDTH = BASE_IMAGE.get_width()
    IMAGE = BASE_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        # Creates and moves two of the same image to the left at a set velocity
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        # If the first image and the screen width are negative (off the screen)
        # Then its put at the position of the second image plus the width of the screen
        # So directly behind it, this creates a constant loop of two images moving across the bottom
        # Of the screen just like a treadmill
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        # This is the same idea just for the second image
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMAGE, (self.x1, self.y))
        win.blit(self.IMAGE, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score, generation):
    # Creates window and sets location and specific image
    win.blit(BACKGROUND_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    text = STAT_FONT.render("Gen: " + str(GEN), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    # Calls draw() function within the bird class
    base.draw(win)

    for bird in birds:
        bird.draw(win)

    pygame.display.update()


def main(genomes, config):
    global GEN
    GEN += 1

    # Stores all data in lists
    nets = []
    ge = []
    birds = []

    # Loop that sets net to the config
    # places it in the nets list
    # Then adds bird object into birds list
    # Defaults fitness value and places the
    # number of loops in the generation list
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]
    run = True
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    score = 0

    # Clock object that uses pygame's fps cap
    clock = pygame.time.Clock()

    # Game loop
    while run:
        # Caps fps to 30 because the fps and game speed are 1 to 1. Higher fps = faster game
        clock.tick(30)
        # Allows loop to break if user quits pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # ALL MOVEMENT FUNCTION CALLS
        # bird.move()

        pipes_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipes_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            # Gives 0.01 points for every second alive
            ge[x].fitness += 0.01

            output = nets[x].activate(
                (bird.y, abs(bird.y - pipes[pipes_ind].height), abs(bird.y - pipes[pipes_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        # THIS IS FOR PIPE
        add_pipe = False
        remove = []
        for pipe in pipes:

            for x, bird in enumerate(birds):

                if pipe.collide(bird):
                    # Every time a bird hits a pipe its fitness score decreases by 1
                    # ge[x].fitness -= 1
                    # Removes dead bird from all lists so a new one can take its place
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            # If birds makes it through pipe its fitness in increased by 5
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for r in remove:
            pipes.remove(r)
        # END OF PIPE

        for x, bird in enumerate(birds):
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
                pass

        base.move()

        draw_window(win, birds, pipes, base, score, GEN)


# AI SET UP

# Connects both this python file and the NEAT config file
# The way NEAT recommends
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    # Sets pop to NEAT's preconfigured population number
    pop = neat.Population(config)

    # Records and prints out population stats
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    # Uses defined population variable in conjunction with the main game loop to
    # Iterate tha main loop 50 times for the AI to learn from
    winner = pop.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedfoward.txt")
    run(config_path)
