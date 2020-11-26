import numpy
import copy


# board should be a 10*10 list
def get_rest_position(board):
    # select all the possible location for next move
    legalPositionList = []
    for i in range(10):
        for j in range(10):
            if board[i][j] == '?':
                if i > 0:
                    if board[i - 1][j] != '?' and (i, j) not in legalPositionList:
                        legalPositionList.append((i, j))
                if i > 0 and j > 0:
                    if board[i - 1][j - 1] != '?' and (i, j) not in legalPositionList:
                        legalPositionList.append((i, j))
                if i > 0 and j < 9:
                    if board[i - 1][j + 1] != '?' and (i, j) not in legalPositionList:
                        legalPositionList.append((i, j))
                if i < 9:
                    if board[i + 1][j] != '?' and (i, j) not in legalPositionList:
                        legalPositionList.append((i, j))
                if i < 9 and j > 0:
                    if board[i + 1][j - 1] != '?' and (i, j) not in legalPositionList:
                        legalPositionList.append((i, j))
                if i < 9 and j < 9:
                    if board[i + 1][j + 1] != '?' and (i, j) not in legalPositionList:
                        legalPositionList.append((i, j))
                if j > 0:
                    if board[i][j - 1] != '?' and (i, j) not in legalPositionList:
                        legalPositionList.append((i, j))
                if j < 9:
                    if board[i][j + 1] != '?' and (i, j) not in legalPositionList:
                        legalPositionList.append((i, j))
    legalPositionList.sort
    return legalPositionList


# position is the point we want to test for score.
# position should be a list, include 2 elements, one for row No. and one for col No.
def get_score(position, board):
    tempBoard = copy.deepcopy(board)
    # A represent computer chess
    tempBoard[position[0]][position[1]] = 'A'

    # For all points, we have 4 possible directions to create a set.
    # Horizontal, vertical, left diagonal, right diagonal
    horizontalLine = ''
    for i in tempBoard[position[0]]:
        horizontalLine += str(i)

    verticalLine = ''

    for i in range(10):
        verticalLine += str(tempBoard[i][position[1]])

    '''
    * . . .
    . * . .
    . . * . 
    . . . *
    '''
    leftToRightDiagonal = ''
    for i in range(10):
        if 10 > i - position[0] + position[1] >= 0:
            leftToRightDiagonal += str(tempBoard[i][i - position[0] + position[1]])

    '''
        . . . *
        . . * .
        . * . . 
        * . . .
    '''
    rightToLeftDiagonal = ''
    for i in range(10):
        if 10 > position[0] + position[1] - i >= 0:
            rightToLeftDiagonal += str(tempBoard[i][position[0] + position[1] - i])

    # Here we should separate different set: Almost five, Live four, Close four A,
    # Close four B, Close four C, Live 3, Close 3 A, Close 3 B, Close 3 C,
    # Close 3 D, Close 3 E, Close 3 F, Live 2, Close 2 A, Close 2 B, Close 2 C
    # Citation1: https://wenku.baidu.com/view/79d2304a8762caaedc33d422.html
    # Citation2: http://game.onegreen.net/wzq/HTML/142336.html
    lineList = [horizontalLine, verticalLine, leftToRightDiagonal, rightToLeftDiagonal]
    totalScore = 0

    # AlmostFive
    for i in lineList:
        if 'AAAAA' in i:
            totalScore += 1000000
            break

    # Live Four
    for i in lineList:
        if '?AAAA?' in i:
            totalScore += 1000000
            break

    # Close Four A
    for i in lineList:
        if 'BAAAA?' in i:
            totalScore += 25000
            break
    # Close Four B
    for i in lineList:
        if 'A?AAA' in i:
            totalScore += 25000
            break
    # Close Four C
    for i in lineList:
        if 'AA?AA' in i:
            totalScore += 25000
            break
    # Close Four D
    for i in lineList:
        if '?AAAAB' in i:
            totalScore += 25000
            break
    # Close Four E
    for i in lineList:
        if 'AAA?A' in i:
            totalScore += 25000
            break

    # Live three A
    for i in lineList:
        if '?AAA?' in i:
            totalScore += 8000
            break
    # Live three B
    for i in lineList:
        if 'A?AA' in i:
            totalScore += 8000
            break
    # Live three C
    for i in lineList:
        if 'AA?A' in i:
            totalScore += 8000
            break

    # Close three A-G
    count = 0
    for i in lineList:
        if '??AAAB' or '?A?AAB' or '?AA?AB' or 'A??AA' or 'A?A?A' or 'B?AAA?B' in i:
            if count < 2:
                count += 1
                totalScore += 5000
            else:
                break

    # Live two
    for i in lineList:
        if '??AA??' or '?A?A?' or 'A??A' in i:
            totalScore += 3000

    # Close two
    for i in lineList:
        if '???AAB' or '??A?AB' or '?A??AB' or 'A???A' or '?AAB?' in i:
            totalScore += 1500

    # Begin Status
    for i in lineList:
        if "??A??" in i:
            totalScore += 100
    return totalScore


# For calculating the enemy score. True score = Computer Score - Human Score(enemy).
def exchangePositionForStone(board):
    tempBoard = copy.deepcopy(board)
    for i in range(10):
        for j in range(10):
            if tempBoard[i][j] == 'A':
                tempBoard[i][j] = 'B'
            elif tempBoard[i][j] == 'B':
                tempBoard[i][j] = 'A'
    return tempBoard


def evaluation(board):
    # Attack
    temp1 = 0
    temp2 = 0
    for i in range(10):
        for j in range(10):
            if board[i][j] == 'A':
                temp1 += get_score([i,j],board)
            if board[i][j] == 'B':
                temp2 += get_score([i,j],board)
    score = temp2 - temp1
    return score
'''
    # Defensive
    position = get_rest_position(board)
    score = 0
    for i in position:
        enemyBoard = exchangePositionForStone(board)
        temp = get_score(i, enemyBoard)*1.2 - get_score(i,board)
        if temp > score:
            score = temp

    return score
'''

# Input:Board,color
# Return True and a string include who win the game when there is a five on the board
# Return False and "still playable" when there still nothing
# Return True and a string "Draw" when there are no position to move and no one wins at last
# citation: https://cloud.tencent.com/developer/article/1537206
def winCheck(board, color):
    for i in range(10):
        for j in range(10):
            # col
            if i < 10 - 4 and board[i][j] == color and board[i + 1][j] == color and board[i + 2][j] == color and \
                    board[i + 3][j] == color and board[i + 4][j] == color:
                return True
            # row
            elif j < 10 - 4 and board[i][j] == color and board[i][j + 1] == color and board[i][j + 2] == color and \
                    board[i][j + 3] == color and board[i][j + 4] == color:
                return True
            elif i < 10 - 4 and j < 10 - 4 and board[i][j] == color and board[i + 1][j + 1] == color and board[i + 2][
                j + 2] == color and board[i + 3][j + 3] == color and board[i + 4][j + 4] == color:
                return True
            elif i > 3 and j < 10 - 4 and board[i][j] == color and board[i - 1][j + 1] == color and board[i - 2][
                j + 2] == color and board[i - 3][j + 3] == color and board[i - 4][j + 4] == color:
                return True
    return False


def drawCheck(board):
    count = 0
    for i in range(10):
        for j in range(10):
            if board[i][j] != "?":
                count += 1
    if count == 100:
        return True
    else:
        return False


# You should input a board like this.

'''testlist = [[?, A,B, B, B, B, B, B, B, ?],
            [?, ?, ?, ?, ?, ?, ?, ?, ?, ?],
            [?, ?, ?, ?, ?, ?, ?, ?, ?, ?],
            [?, ?, ?, ?, ?, ?, ?, ?, ?, ?],
            [?, ?, ?, ?, ?, ?, ?, ?, ?, ?],
            [?, ?, ?, ?, ?, ?, ?, ?, ?, ?],
            [?, ?, ?, ?, ?, ?, ?, ?, ?, ?],
            [?, ?, ?, ?, ?, ?, ?, ?, ?, ?],
            [?, ?, ?, ?, ?, ?, ?, ?, ?, ?],
            [?, ?, ?, ?, ?, ?, ?, ?, ?, ?]]
print(str(testlist[0]))
temp = ''
for i in testlist[0]:
    temp += str(i)
print(temp)
print(str(testlist[0])[1: -1].replace(',', '').replace(' ', ''))'''
