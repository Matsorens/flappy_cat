import pygame
import random

win_width, win_height = 500, 480

# Inilitialise screen
pygame.init()
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("First Game")
clock = pygame.time.Clock()
# -------------------

# Images and music
music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

bg = pygame.image.load("space.jpg")
game_over = pygame.image.load("game_over.png")
cat = pygame.image.load("cat2.png")
# laserbeam = pygame.image.load("laserbeam1.png")

# Blockcontainer
block_lst = list()


def main():
    # Functionality: gameplay, main-loop and eventcontroll

    # Variables
    x_position = 80                             # initial x-position bird
    initial_y_pos = int(win_height/10)          # initial y-position bird
    y_value = initial_y_pos                     # variabele y-value
    jump_max_height = 6                         # maximum height of each jump
    jump_height_current = 0                     # current jumpheight during a jump
    jump_speed = 20                             # speed during the jump
    gravity = 0                                 # container for gravity variable (decreasing)
    time_count = 0                              # counter for when to add new blocks
    jump = False                                # determine when to stop jump
    finish = False                              # changes to True when game over
    points = 0                                  # variable counting points

    # Main loop
    run = True
    while run:
        clock.tick(30)  # FPS

        # gravity constantly decreasing the y position (therefore +), despite when jumping
        if not jump:
            gravity += 10

        # Block generator
        time_count += 1 # Time count to determine when to make a new block

        if time_count % 37 == 0:
            new_block()

        # Moving blocks
        for blocks in block_lst:
            blocks[0] -= 5

            # deleting passed blocks in block_lst
            if blocks[0] < -40:
                block_lst.pop()
                block_lst.pop()

        # calculating y-position of the circle
        y_position = int(win_height / 2) - y_value + gravity

        # Event: Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Event: Spacebar = Jump
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            jump = True

        if jump:
            y_value += jump_speed
            jump_height_current += 1

            if jump_height_current == jump_max_height:
                jump_height_current = 0
                jump = False

        # Game over
        # colission with wall
        if y_position < 0 or y_position > win_height:
            finish = True

        # collission with block
        for block in block_lst:
            # collision with upper block
            if block[0] < x_position < block[0] + block[2] and block[1] < y_position  < block[1] + block[3]:
                # print("hit")
                finish = True

            # collision with lower block
            if block[0] < x_position < block[0] + block[2] and block[1] > y_position > block[1] + block[3]:
                # print("hit")
                finish = True

            # Points
            if not finish:
                if block[0] < x_position < block[0] + 10:
                    points += 0.5   # 0.5 because it will apply for both upper and lower block

        # Redraw gamewindow
        redraw_game_window(x_position, y_position, block_lst, finish, int(points))


# function drawing shapes
def redraw_game_window(x, y, blocks, finish, points):
    # Reset window
    #win.fill((0,0,0))
    win.blit(bg, (0,0))

    if not finish:
        # Drawign circle - the bird
        win.blit(cat, (x-15, y-15))
        # pygame.draw.rect(win, (255, 255, 0), (x-10, y-10, 20, 20), 2)     # hitbox

        # Drawing blocks
        for block in blocks:
            pygame.draw.rect(win, (179, 30, 253), (block[0], block[1], block[2], block[3]))
            pygame.draw.rect(win, (0, 0, 0), (block[0], block[1], block[2]+2, block[3]), 4)

        # Drawing text
        font = pygame.font.SysFont("comicsansms", 25, True)
        point_text = font.render("Points: " + str(points), 1, (255, 255, 255))
        win.blit(point_text, (10, 10))

    elif finish:
        # Drawing text - "game over" and "points"
        win.blit(game_over, (-30, 100))
        font = pygame.font.SysFont("comicsansms", 50, True)
        text = font.render("GAME OVER", 1, (255, 255, 255))
        font = pygame.font.SysFont("comicsansms", 20, True)
        text_point = font.render("SCORE: " + str(points), 1, (255, 255, 255))
        win.blit(text, (win_width/2 - 150, win_height/2 - 50))
        win.blit(text_point, (win_width / 2 - 150, win_height / 2 + 20))

    pygame.display.update()


# function adding new blocks to block_lst
def new_block():
    # [x, y, width, height]
    # inserting upper block
    block_lst.insert(0, [win_width-30, 0, 30, random.randint(50, 210)])

    # inserting lower block
    block_lst.insert(0, [win_width-30, win_height, 30, random.randint(-210, -50)])


main()


