# Nathan Boyden
# 5/21/2024
# Pong in Python using the pygame library
import sys, pygame, random, asyncio

# initializes the pygame renderer
pygame.init()


def reset_ball():
    global ball_speed_y, ball_speed_x

    ball.x = screen_width / 2 - 10
    ball.y = random.randint(10, 100)

    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])


def point_won(winner):
    global cpu_points, player_points
    if winner == "cpu":
        cpu_points += 1
    if winner == "player":
        player_points += 1

    reset_ball()


def animate_ball():
    # Makes these two variables usable anywhere in the code
    global ball_speed_x, ball_speed_y

    # Changes ball position in-game
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # This makes the ball "bounce" off the edges of the window
    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    if ball.right >= screen_width:
        point_won("cpu")

    if ball.left <= 0:
        point_won("player")

    if ball.colliderect(player) or ball.colliderect(cpu):
        ball_speed_x *= -1


def animate_player():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0

    if player.bottom >= screen_height:
        player.bottom = screen_height


def animate_cpu():
    global cpu_speed

    cpu.y += cpu_speed

    if ball.centery <= cpu.centery:
        cpu_speed = -6
    if ball.centery >= cpu.centery:
        cpu_speed = 6

    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height


# Defines the display resolution in pixels by pixels
screen_width = 1280
screen_height = 800

# Creates and displays a blank screen with the resolution defined earlier
screen = pygame.display.set_mode((screen_width, screen_height))

# Gives window a caption
pygame.display.set_caption("Pong")

# Defines frame rate for game
clock = pygame.time.Clock()

# Ball object
ball = pygame.Rect(0, 0, 30, 30)
ball.center = (screen_width / 2, screen_height / 2)

cpu = pygame.Rect(0, 0, 20, 100)
cpu.centery = (screen_height / 2)

player = pygame.Rect(0, 0, 20, 100)
player.midright = (screen_width, screen_height / 2)

# Game attributes
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
cpu_speed = 2

cpu_points, player_points = 0, 0

# defines font and size of text for UI in-game
score_font = pygame.font.Font(None, 100)

# Game loop
while True:
    # For every event pygame tracks it will scan it and check if its of type quit
    # If so it will force pygame to quit then the system to quit ending the game loop
    # Also deals with input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Takes input using pygame and checks whether to up or down key is being pressed then set
        # the speed of the player block to -6 (up) or 6(down) and stops (0) when key is released
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -6
            if event.key == pygame.K_DOWN:
                player_speed = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed = 0
            if event.key == pygame.K_DOWN:
                player_speed = 0

    # Animation functions
    animate_ball()
    animate_player()
    animate_cpu()

    # Removes previous frame's objects to prevent ghosting
    screen.fill('black')

    # Draws in-game UI
    cpu_score_surface = score_font.render(str(cpu_points), True, "white")
    player_score_surface = score_font.render(str(player_points), True, "white")
    screen.blit(cpu_score_surface, (screen_width / 4, 20))
    screen.blit(player_score_surface, (3 * screen_width / 4, 20))

    # Draw the game objects
    pygame.draw.aaline(screen, 'white', (screen_width / 2, 0), (screen_width / 2, screen_height))
    pygame.draw.ellipse(screen, 'white', ball)
    pygame.draw.rect(screen, 'white', cpu)
    pygame.draw.rect(screen, 'white', player)

    # Updates screen with objects
    pygame.display.update()

    # Sets fps to 60 within the game loop
    clock.tick(75)
