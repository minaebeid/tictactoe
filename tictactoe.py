import sys
import copy
import random
import pygame
import numpy as np

from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BG_COLOR)

class Board:

    def __init__(self) -> None:
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_squares = self.squares
        self.marked_squares = 0
        print(self.squares)

    def final_state(self):
        # Vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
            
        # Horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[0][row]
            
        # Diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]
        
        # no win yet
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def empty_square(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))
        return empty_squares

    def isfull(self):
        return self.marked_squares == 9
    
    def isempty(self):
        return self.marked_squares == 0

class AI:

    def __init__(self, level = 1, player = 2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0, len(empty_squares))

        return empty_squares[index]

    def minimax(self, board, maximizing):
        # End game case
        case = board.final_state()

        #player 1 wins
        if case == 1:
            return 1, None
        #player 2 wins
        if case == 2:
            return -1, None
        elif board.isfull():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row,col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move
        
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row,col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            pass
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f"AI has chosen the square {move} with an eval of {eval}")
        return move # row , col
        

class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()

    def show_lines(self):
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_figure(self, row, col):
        if self.player == 1:
            # draw a cross
            start_d =(col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_d = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            start_a = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_a = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_d, end_d, CROSS_WIDTH)
            pygame.draw.line(screen, CROSS_COLOR, start_a, end_a, CROSS_WIDTH)
        elif self.player == 2:
            # draw a circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

    def next_turn(self):
        self.player = (self.player % 2) + 1

def main():

    game = Game()
    board = game.board
    ai = game.ai
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_square(row,col):
                    board.mark_square(row, col, game.player)
                    game.draw_figure(row, col)
                    game.next_turn()

        if game.gamemode == 'ai' and game.player == ai.player:
            # update the screen
            pygame.display.update()

            # ai methods
            row, col = ai.eval(board)

            board.mark_square(row, col, ai.player)
            game.draw_figure(row, col)
            game.next_turn()

        pygame.display.update()
main()