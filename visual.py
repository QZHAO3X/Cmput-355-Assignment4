import pygame
import sys
import calculation
import alphabeta_new as alphabeta
import numpy as np
from pygame.locals import *

from tkinter import messagebox

'''References:
    1. https://www.pygame.org/docs/
'''
'''
Black stone (B) is user and white stone (A) is program
'''

# Initialize the module, window, font and set the title
pygame.init()
font = pygame.font.Font('SourceSansProItalic.ttf', 15)
size = 500, 500  # size of screen
screen = pygame.display.set_mode(size)  # set the window size as 500*500
pygame.display.set_caption('Gomoku')

# Create a numpy array with '?' for empty board
initial_board = [['?', '?', '?', '?', '?', '?', '?', '?', '?', '?'],
                 ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?'],
                 ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?'],
                 ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?'],
                 ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?'],
                 ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?'],
                 ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?'],
                 ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?'],
                 ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?'],
                 ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?']]

# Initialize the screen, black and white stones
white = [255, 255, 255]  # Set the color of white stones in RGB mode
black = [0, 0, 0]  # Set the color of black stones in RGB mode
brown = [153, 76, 0]  # Set the background color of board in RGB mode
w_stone = 'A'
b_stone = 'B'
radius = 10
width = 0
screen.fill(brown)

# Set the start and end positions for horizontal and vertical lines
x_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
y_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
h_start = [70, 70]
h_end = [430, 70]
v_start = [70, 70]
v_end = [70, 430]

# Create a dictionary to store the coordinate of each position
stone_position = {}
index_list = {}
v_list = []  # For the name of coordinate vertically sorted
h_list = []  # For the name of coordinate horizontally sorted


# Draw a 10x10 board
def board():
    # Draw 10 lines for both x and y axis
    global v_start, h_end, v_end, h_start
    for i in range(10):
        pygame.draw.line(screen, black, h_start, h_end, 1)
        pygame.draw.line(screen, black, v_start, v_end, 1)

        # Update the start and end positions for both next lines
        h_start = [70, h_start[1] + 40]
        h_end = [430, h_end[1] + 40]
        v_start = [v_start[0] + 40, 70]
        v_end = [v_end[0] + 40, 430]

    # Set the x and y axis name
    h_start1 = [70, 35]
    v_start1 = [45, 60]
    for i in range(len(x_list)):
        x_name = font.render(x_list[i], True, black)
        y_name = font.render(y_list[i], True, black)
        screen.blit(x_name, h_start1)
        screen.blit(y_name, v_start1)
        h_start1 = [h_start1[0] + 40, 35]
        v_start1 = [45, v_start1[1] + 40]

    # Initialize x and y coordinates
    x = 70
    y = 70

    # Insert the key and content into 'combine' dictionary
    for i in range(len(x_list)):
        for j in range(len(y_list)):
            name = x_list[i] + y_list[j]
            stone_position[name] = [x, y]
            index_list[name] = [j, i]
            y += 40
        x += 40
        y = 70  # Reset y to the top

    # Put keys of dictionary into a list and remove 4 corners
    for i in stone_position.keys():
        v_list.append(i)
    v_list.remove('A1')
    v_list.remove('A10')
    v_list.remove('J1')
    v_list.remove('J10')

    # Insert h_list same as v_list
    for j in range(len(y_list)):
        for i in range(len(x_list)):
            h_list.append(x_list[i] + y_list[j])
    h_list.remove('A1')
    h_list.remove('A10')
    h_list.remove('J1')
    h_list.remove('J10')


def position_checker(coord):
    # Check if the position of coordinate belongs to which point
    x_point = coord[0]
    y_point = coord[1]

    # Set 4 corners position
    if x_point < 90 and y_point < 90:
        if initial_board[0][0] == '?':
            pygame.draw.circle(screen, black, stone_position['A1'], radius, width)
            initial_board[0][0] = b_stone  # Exchange the empty cell as black stone
            pygame.display.update()

            if calculation.winCheck(initial_board, "B"):
                messagebox.showinfo('Result', 'Black wins!')
            else:
                # Computer ('A') makes move (White stone)
                calculation.get_rest_position(initial_board)  # Get all empty cells
                w_position = alphabeta.minmax(initial_board, 3)  # Get the white stone position eg:(0, 0)
                pos = search_key([w_position[0], w_position[1]])
                pygame.draw.circle(screen, white, stone_position[pos], radius, width)  # Draw the white stone
                # Exchange the empty cell as white stone
                initial_board[w_position[0]][w_position[1]] = w_stone  # Exchange the empty cell as black stone

    if x_point < 90 and y_point > 410:
        if initial_board[9][0] == '?':
            pygame.draw.circle(screen, black, stone_position['A10'], radius, width)
            initial_board[9][0] = b_stone  # Exchange the empty cell as black stone
            pygame.display.update()

            if calculation.winCheck(initial_board, "B"):
                messagebox.showinfo('Result', 'Black wins!')
            else:
                # Computer ('A') makes move (White stone)
                calculation.get_rest_position(initial_board)  # Get all empty cells
                w_position = alphabeta.minmax(initial_board, 3)  # Get the white stone position eg:(0, 0)
                pos = search_key([w_position[0], w_position[1]])
                pygame.draw.circle(screen, white, stone_position[pos], radius, width)  # Draw the white stone
                # Exchange the empty cell as white stone
                initial_board[w_position[0]][w_position[1]] = w_stone  # Exchange the empty cell as black stone

    if x_point > 410 and y_point < 70:
        if initial_board[0][9] == '?':
            pygame.draw.circle(screen, black, stone_position['J1'], radius, width)
            initial_board[0][9] = b_stone  # Exchange the empty cell as black stone
            pygame.display.update()

            if calculation.winCheck(initial_board, "B"):
                messagebox.showinfo('Result', 'Black wins!')
            else:
                # Computer ('A') makes move (White stone)
                calculation.get_rest_position(initial_board)  # Get all empty cells
                w_position = alphabeta.minmax(initial_board, 3)  # Get the white stone position eg:(0, 0)
                pos = search_key([w_position[0], w_position[1]])
                pygame.draw.circle(screen, white, stone_position[pos], radius, width)  # Draw the white stone
                # Exchange the empty cell as white stone
                initial_board[w_position[0]][w_position[1]] = w_stone  # Exchange the empty cell as black stone

    if x_point > 410 and y_point > 410:
        if initial_board[9][9] == '?':
            pygame.draw.circle(screen, black, stone_position['J10'], radius, width)
            initial_board[9][9] = b_stone  # Exchange the empty cell as black stone
            pygame.display.update()

            if calculation.winCheck(initial_board, "B"):
                messagebox.showinfo('Result', 'Black wins!')
            else:
                # Computer ('A') makes move (White stone)
                calculation.get_rest_position(initial_board)  # Get all empty cells
                w_position = alphabeta.minmax(initial_board, 3)  # Get the white stone position eg:(0, 0)
                pos = search_key([w_position[0], w_position[1]])
                pygame.draw.circle(screen, white, stone_position[pos], radius, width)  # Draw the white stone
                # Exchange the empty cell as white stone
                initial_board[w_position[0]][w_position[1]] = w_stone  # Exchange the empty cell as black stone

    # Set points on 4 edges position
    # Left: A2-A9
    lx = 90
    ly1 = 90
    ly2 = 130
    for i in range(8):
        if x_point < lx and ly1 < y_point < ly2:
            h = index_list[v_list[i]][0]
            v = index_list[v_list[i]][1]
            if initial_board[h][v] == '?':
                pygame.draw.circle(screen, black, stone_position[v_list[i]], radius, width)
                initial_board[h][v] = b_stone  # Exchange the empty cell as black stone
                pygame.display.update()

                if calculation.winCheck(initial_board, "B"):
                    messagebox.showinfo('Result', 'Black wins!')
                    break
                else:
                    # Computer ('A') makes move (White stone)
                    calculation.get_rest_position(initial_board)  # Get all empty cells
                    w_position = alphabeta.minmax(initial_board, 3)  # Get the white stone position eg:(0, 0)
                    pos = search_key([w_position[0], w_position[1]])
                    pygame.draw.circle(screen, white, stone_position[pos], radius, width)  # Draw the white stone
                    # Exchange the empty cell as white stone
                    initial_board[w_position[0]][w_position[1]] = w_stone  # Exchange the empty cell as black stone
            break
        else:
            ly1 += 40
            ly2 += 40

    # Top: B1 - I1
    tx1 = 90
    tx2 = 130
    ty = 90
    for j in range(8):
        if tx1 < x_point < tx2 and y_point < ty:
            h = index_list[h_list[j]][0]
            v = index_list[h_list[j]][1]
            if initial_board[h][v] == '?':
               pygame.draw.circle(screen, black, stone_position[h_list[j]], radius, width)
               initial_board[h][v] = b_stone  # Exchange the empty cell as black stone
               pygame.display.update()

               if calculation.winCheck(initial_board, "B"):
                   messagebox.showinfo('Result', 'Black wins!')
                   break
               else:
                   # Computer ('A') makes move (White stone)
                   calculation.get_rest_position(initial_board)  # Get all empty cells
                   w_position = alphabeta.minmax(initial_board, 3)  # Get the white stone position eg:(0, 0)
                   pos = search_key([w_position[0], w_position[1]])
                   pygame.draw.circle(screen, white, stone_position[pos], radius, width)  # Draw the white stone
                   # Exchange the empty cell as white stone
                   initial_board[w_position[0]][w_position[1]] = w_stone  # Exchange the empty cell as black stone
            break
        else:
            tx1 += 40
            tx2 += 40

    # Right: J2 - J9
    rx = 410
    ry1 = 90
    ry2 = 130
    for j in range(88, 96):
        if x_point > rx and ry1 < y_point < ry2:
            h = index_list[v_list[j]][0]
            v = index_list[v_list[j]][1]
            if initial_board[h][v] == '?':
                pygame.draw.circle(screen, black, stone_position[v_list[j]], radius, width)
                initial_board[h][v] = b_stone  # Exchange the empty cell as black stone
                pygame.display.update()

                if calculation.winCheck(initial_board, "B"):
                    messagebox.showinfo('Result', 'Black wins!')
                    break
                else:
                    # Computer ('A') makes move (White stone)
                    calculation.get_rest_position(initial_board)  # Get all empty cells
                    w_position = alphabeta.minmax(initial_board, 3)  # Get the white stone position eg:(0, 0)
                    pos = search_key([w_position[0], w_position[1]])
                    pygame.draw.circle(screen, white, stone_position[pos], radius, width)  # Draw the white stone
                    # Exchange the empty cell as white stone
                    initial_board[w_position[0]][w_position[1]] = w_stone  # Exchange the empty cell as black stone
            break
        else:
            ry1 += 40
            ry2 += 40

    # Bottom: B10 - I10
    bx1 = 90
    bx2 = 130
    by = 410
    for j in range(88, 96):
        if bx1 < x_point < bx2 and y_point > by:
            h = index_list[h_list[j]][0]
            v = index_list[h_list[j]][1]
            if initial_board[h][v] == '?':
                pygame.draw.circle(screen, black, stone_position[h_list[j]], radius, width)
                initial_board[h][v] = b_stone  # Exchange the empty cell as black stone
                pygame.display.update()

                if calculation.winCheck(initial_board, "B"):
                    messagebox.showinfo('Result', 'Black wins!')
                    break
                else:
                    # Computer ('A') makes move (White stone)
                    calculation.get_rest_position(initial_board)  # Get all empty cells
                    w_position = alphabeta.minmax(initial_board, 3)  # Get the white stone position eg:(0, 0)
                    pos = search_key([w_position[0], w_position[1]])
                    pygame.draw.circle(screen, white, stone_position[pos], radius, width)  # Draw the white stone
                    # Exchange the empty cell as white stone
                    initial_board[w_position[0]][w_position[1]] = w_stone  # Exchange the empty cell as black stone
            break
        else:
            bx1 += 40
            bx2 += 40

    # Middle part of board from B2-I9
    mx1 = 90
    mx2 = 130
    for i in range(1, len(x_list)):
        my1 = 90
        my2 = 130
        for j in range(1, len(y_list)):
            if mx1 < x_point < mx2 and my1 < y_point < my2:
                h = index_list[x_list[i] + y_list[j]][0]
                v = index_list[x_list[i] + y_list[j]][1]
                if initial_board[h][v] == '?':
                    pygame.draw.circle(screen, black, stone_position[x_list[i] + y_list[j]], radius, width)
                    initial_board[h][v] = b_stone  # Exchange the empty cell as black stone
                    pygame.display.update()

                    if calculation.winCheck(initial_board, "B"):
                        messagebox.showinfo('Result', 'Black wins!')
                        break
                    else:
                        # Computer ('A') makes move (White stone)
                        calculation.get_rest_position(initial_board)  # Get all empty cells
                        w_position = alphabeta.minmax(initial_board, 3)  # Get the white stone position eg:(0, 0)
                        pos = search_key([w_position[0], w_position[1]])
                        pygame.draw.circle(screen, white, stone_position[pos], radius, width)  # Draw the white stone
                        # Exchange the empty cell as white stone
                        initial_board[w_position[0]][w_position[1]] = w_stone  # Exchange the empty cell as black stone
                break
            else:
                my1 += 40
                my2 += 40
        mx1 += 40
        mx2 += 40


def search_key(value):
    for k, val in index_list.items():
        if value == val:
            return k


def play():
    # Get the board
    global initial_board
    board()

    # Start the pygame
    while True:
        # If user pressed the left key, the stone will be put on the board
        pressed = False

        # Get the user actions
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                pressed = True
            if event.type is QUIT:
                sys.exit()

        # Get the mouse position
        coord = pygame.mouse.get_pos()

        if pressed:
            # User ('B') makes move (Black stone)
            position_checker(coord)
            pygame.display.update()

            pygame.display.update()
            # Win or lose
            if calculation.winCheck(initial_board, "A"):
                messagebox.showinfo('Result', 'White wins!')
                break
        if calculation.drawCheck(initial_board):
            messagebox.showinfo('Result', 'Draw!')
            break
        pygame.display.update()


def main():
    play()


main()
