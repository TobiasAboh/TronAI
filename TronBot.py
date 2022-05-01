import curses
from curses import wrapper
import random
import sys
import math
import numpy as np
from copy import deepcopy
from time import time, sleep


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
board  = [[0 for j in range(30)] for i in range(20)]
def showscreen(stdscr, p_board):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)

    
    for i in range(len(p_board)):
        for j in range(len(p_board[i])):
            # print(p_board)
            colour = curses.color_pair(p_board[i][j])
            stdscr.addstr(i, j*2, str(p_board[i][j]), colour)

def updateScreen(stdscr):
    stdscr.clear()
    showscreen(stdscr, board)
    stdscr.refresh()
    stdscr.getch()

class Game:

    def getNeighbours(self, pBoard, x, y):
        neighbours = []
        # print(x, y)
        if y != 0 and pBoard[y - 1][x] == 0:
            neighbours.append("UP")
        if x != 0 and pBoard[y][x - 1] == 0:
            neighbours.append("LEFT")
        if y != (len(pBoard) - 1) and pBoard[y + 1][x] == 0:
            neighbours.append("DOWN")
        if x != (len(pBoard[0]) - 1) and pBoard[y][x + 1] == 0:
            neighbours.append("RIGHT")
        return neighbours

    def updateBoard(self, pBoard, x, y, turn):
        if x != -1 and y != -1: 
            if pBoard[y][x] == 0:
                pBoard[y][x] = turn
        elif (x == -1 and y == -1): #and pBoard.count(id) > 0:
            for i in range(len(pBoard)):
                for j in range(len(pBoard[i])):
                    pBoard[i][j] = 0 if pBoard[i][j] == turn else pBoard[i][j]
                
def convMove(move, x, y):
    if move == "UP":
        return [x, y-1]
    elif move == "LEFT":
        return [x - 1, y]
    elif move == "DOWN":
        return [x, y + 1]
    elif move == "RIGHT":
        return [x + 1, y]

class LightCycle:
    def __init__(self, id, x=0, y=0):
        self.x = x
        self.y = y
        self.id = id
    

def floodFill(game, pBoard, playerInfoList):
    fakeBoard = deepcopy(pBoard)
    q = [playerInfoList[x] + [x] for x in playerInfoList if playerInfoList[x] != [-1, -1]]
    scores = [0 for i in range(len(playerInfoList))]
    
    while len(q) != 0:
        # for player in playerList:
        # print(q)
        curr = q[0]
        # print(curr)
        q.remove(q[0])
        moves = game.getNeighbours(fakeBoard, curr[0], curr[1])
        
        for i in range(len(moves)):
            direction = convMove(moves[i], curr[0], curr[1])
            if fakeBoard[direction[1]][direction[0]] == 0: 
                # print(curr, file=sys.stderr, flush=True) 
                q.append(direction + [curr[2]])
                scores[curr[2]-1] += 1
                game.updateBoard(fakeBoard, direction[0], direction[1], curr[2])
    # print(scores)
    return scores



class State:
    def __init__(self, board, positions, turn):
        self.board = board
        self.positions = positions
        self.turn = turn

    def nextTurn(self):
        turn = (self.turn + 1) if self.turn + 1 <= len(self.positions) else 1
        # print(turn)
        while self.positions[turn] == [-1, -1]:
            turn = (turn + 1) if turn + 1 <= len(self.positions) else 1
        return turn

    def evaluate(self):
        lastManStanding = [x for x in self.positions if self.positions[x] != [-1, -1]]
        return lastManStanding[0] if len(lastManStanding) == 1 else None

def simulate(game, state, move):
    newState = State(deepcopy(state.board), deepcopy(state.positions), state.turn)
    currPos = newState.positions[newState.turn]

    if len(game.getNeighbours(newState.board, currPos[0], currPos[1])) == 0:
        newState.positions[newState.turn] = [-1, -1]
        game.updateBoard(newState.board, -1, -1, newState.turn)
        newState.turn = newState.nextTurn()
    else:
        newPos = convMove(move, currPos[0], currPos[1])
        newState.positions[newState.turn] = newPos
        game.updateBoard(newState.board, newPos[0], newPos[1], newState.turn)
        newState.turn = newState.nextTurn()

    return newState


def maxn2(game, state, depth, start, limit):
    if (time() - start) * 1000 > limit:
        return ['abort', -123]
    if state.evaluate() == state.turn:
        score = [0 for i in range(len(state.positions))]
        score[state.turn - 1] = float('inf')
        
        return ['', score]
    
    if depth <= 0:
        return ['', floodFill(game, state.board, state.positions)]
    bestMove = ''
    bestScore = [float('-inf') for i in range(len(state.positions))]
    copyState = deepcopy(state)

    children = game.getNeighbours(copyState.board, copyState.positions[copyState.turn][0], copyState.positions[copyState.turn][1])
    if not children:
        children = ['UP']
    for i in range(len(children)):
        newState = simulate(game, copyState, children[i])
        score = maxn2(game, newState, depth-1, start, limit)[1]
        if score == -123:
            return ['abort', -123]
        
        if score[copyState.turn - 1] > bestScore[copyState.turn - 1]:
            bestScore = score
            bestMove = children[i]
        if depth == 1000:
            print([bestMove, bestScore])

    return [bestMove, bestScore]
    
def ids(game, state, timeLimit):
    startTime = time()
    d = 1
    move = ""
    bScore = []

    while ((time() - startTime) * 1000) < timeLimit:
        result = maxn2(game, state, d, startTime, timeLimit)
        move, bscore = result if result[0] != 'abort' else [move, bscore]

        d += 1
    return move





def main(stdscr):
    game = Game()
    board = [[0 for i in range(30)] for j in range(20)]
    b1 = [random.randrange(0, 30), random.randrange(0, 20)]
    b2 = [random.randrange(0, 30), random.randrange(0, 20)]
    while b2 == b1:
        b2 = [random.randrange(0, 30), random.randrange(0, 20)]
    players = {1: b1, 2: b2}
    board[b1[1]][b1[0]] = 1
    board[b2[1]][b2[0]] = 2
    state = State(board, players, 1)

    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    while state.positions[state.turn] != [-1, -1]:
        if state.evaluate() != None:
            break
        p1_move = ids(game, state, 100)
        
        stdscr.clear()
        showscreen(stdscr, board)
        stdscr.addstr(state.positions[state.turn][1], state.positions[state.turn][0]*2, "x", curses.color_pair(3))
        stdscr.refresh()

        state = simulate(game, state, p1_move)
        board = state.board

        p2_move = ids(game, state, 100)

        stdscr.clear()
        showscreen(stdscr, board)
        stdscr.addstr(state.positions[state.turn][1], state.positions[state.turn][0]*2, "y", curses.color_pair(4))
        stdscr.refresh()

        state = simulate(game, state, p2_move)
        board = state.board
    stdscr.getch()

wrapper(main)

