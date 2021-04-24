import sys
import pygame
from pygame.locals import *
from Sudoku import Sudoku


def sum_array(my_array: list):
    """Return the sum of a list of numbers."""
    s = 0
    for x in my_array:
        s += x
    return s


# Initialize the game with window size
pygame.init()
size = width, height = (488, 488)
screen = pygame.display.set_mode(size)

squareSize = squareWidth, squareHeight = (50, 50)
spaces = [5, 3, 3, 5, 3, 3, 5, 3, 3]  # exclude the last space.

black = (0, 0, 0)
lightSquareColor = (245, 245, 245)
darkTextColor = (30, 30, 30)
greyTextColor = (75, 75, 75)
redTextColor = (200, 0, 0)
selectedSquareColor = (200, 200, 200)

selectedSquare = -1

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)

myFont = pygame.font.Font(None, 54)

testPuzzleNums = '738510962049307005051020000302700000006402753400600210000200030000030640003905020'
puzzle = Sudoku(testPuzzleNums)

squares = [pygame.Surface(squareSize).convert() for i in range(81)]
for i in range(len(squares)):
    squares[i].fill(lightSquareColor)

numberMap = {K_1: 1, K_KP1: 1, K_2: 2, K_KP2: 2, K_3: 3, K_KP3: 3, K_4: 4, K_KP4: 4, K_5: 5, K_KP5: 5,
             K_6: 6, K_KP6: 6, K_7: 7, K_KP7: 7, K_8: 8, K_KP8: 8, K_9: 9, K_KP9: 9}

# use an index for squares array ... easier than tracking pixel by pixel
selectedSquare = -1  # -1 means none selected .... otherwise should be in range(81)
puzzleCompleted = False

# Start the game loop ... will run forever unless the window is closed
while 1:
    mouseClickPosition = (0, 0)
    # Check for user input events.
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            # print(event.button, event.pos)
            mouseClickPosition = event.pos
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                selectedSquare = -1
            if selectedSquare != -1:  # we only care about the following key presses if a square is currently selected.
                if event.key == K_UP:
                    move_y = selectedSquare - 9
                    if 0 <= move_y <= 80:
                        selectedSquare = move_y
                if event.key == K_DOWN:
                    move_y = selectedSquare + 9
                    if 0 <= move_y <= 80:
                        selectedSquare = move_y
                if event.key == K_LEFT:
                    move_x = selectedSquare - 1
                    if 0 <= move_x <= 80 and selectedSquare % 9 != 0:  # ignoring suggestion for readability.
                        selectedSquare = move_x
                if event.key == K_RIGHT:
                    move_x = selectedSquare + 1
                    if 0 <= move_x <= 80 and selectedSquare % 9 != 8:
                        selectedSquare = move_x
                if event.key in numberMap:
                    puzzle.set_number(selectedSquare, numberMap[event.key])
                if event.key == K_0 or event.key == K_KP0 or event.key == K_DELETE or event.key == K_BACKSPACE:
                    puzzle.set_number(selectedSquare, 0)

    # Update Sudoku to ensure all values have accurate validity.
    puzzleCompleted = puzzle.check_puzzle()

    # update the screen with grid / numbers
    screen.blit(background, (0, 0))
    for r in range(9):
        for c in range(9):
            loc_s = 9 * r + c
            loc_x = squareWidth * c + sum_array(spaces[:c + 1])  # calculate the x,y position of the square on screen.
            loc_y = squareWidth * r + sum_array(spaces[:r + 1])

            # Determine the background color:
            sqrColor = lightSquareColor

            # Determine the text color:
            textColor = darkTextColor  # default
            if puzzle.get_editable(loc_s):
                textColor = greyTextColor
            if not puzzle.get_valid(loc_s):
                textColor = redTextColor

            # Determine if a square is selected:
            if (loc_x <= mouseClickPosition[0] < loc_x + squareWidth) and \
                    (loc_y <= mouseClickPosition[1] < loc_y + squareHeight):
                selectedSquare = loc_s
                mouseClickPosition = (0, 0)  # once the square has been selected, reset the mouse click position
            if selectedSquare == loc_s:
                sqrColor = selectedSquareColor

            # Update the surfaces with proper colors:
            sqr = squares[loc_s]
            sqr.fill(sqrColor)

            number = puzzle.get_number(loc_s)
            if number != 0:
                num = myFont.render(str(number), True, textColor, sqrColor)
                num_x = (sqr.get_width() - num.get_width()) / 2  # calculate center
                num_y = (sqr.get_height() - num.get_height()) / 2 + 3  # calculate "visual" center:
                sqr.blit(num, (num_x, num_y))

            screen.blit(sqr, (loc_x, loc_y))

    # TODO: figure out end
    if puzzleCompleted:
        print(f'You win!')
    pygame.display.flip()
