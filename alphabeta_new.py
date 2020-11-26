# This python file is min/max search
# it include three functions, minmax, min_layer, and max_layer
from calculation import *
import random


def minmax(board, depth):
    bestlist = []
    best = 0
    points = get_rest_position(board)  # get all empty points
    alpha = -99999999
    beta = 99999999
    for i in range(len(points)):
        p = points[i]  # get the position of empty points
        board[p[0]][p[1]] = "B"  # assume that we put into this position
        v = min_layer(board, depth - 1, alpha, beta)
        if v == best:
            bestlist.append(p)  # find all same score positon
        elif v > best:  # if other position have higher score
            best = v
            bestlist = []
            bestlist.append(p)
        board[p[0]][p[1]] = "?"
        # i = i+1
        '''if v > best:
            best = v
        if best > beta:
            return best
        alpha = max(alpha, best)'''

    result = random.choice(bestlist)  # choose a position randomly
    return result


# min function
def min_layer(board, depth, alpha, beta):
    v = evaluation(board)
    if depth == 0:
        #print(v)
        return v
    best = 1000000
    points = get_rest_position(board)  # get all points that are empty
    for i in range(len(points)):
        p = points[i]  # get the position of empty points
        board[p[0]][p[1]] = "A"
        if best < alpha:
            v = max_layer(board, depth-1,best, beta)
        else:
            v = max_layer(board, depth-1, alpha, beta)
        board[p[0]][p[1]] = "?"
        # i=i+1
        if v < best:
            best = v
        if v > alpha:
            alpha = best
            break
        #beta = min(beta, best)
    return best


# max function
def max_layer(board, depth, alpha, beta):
    v = evaluation(board)
    if depth == 0:
        #print(v)
        return v
    best = 0
    points = get_rest_position(board)
    for i in range(len(points)):
        p = points[i]
        board[p[0]][p[1]] = "B"
        if best > beta:
            v = min_layer(board, depth - 1, alpha, best)
        else:
            v = min_layer(board, depth - 1, alpha, beta)
        board[p[0]][p[1]] = "?"
        # i = i+1
        if v > best:
            best = v
        if v < beta:
            beta = best
            break
        #alpha = max(alpha, best)
    return best
