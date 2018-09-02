# coding:utf-8  # For: SyntaxError: Non-ASCII character
import copy
import random

BOARD_SIZE = 8
BLACK = 1
WHITE = 0
NONE = -1


class Player:
    color = BLACK
    board = []

    def __init__(self, color):
        # Constructor
        self.color = color

    def get_board(self, board):
        # Get Board Data from Othello Class
        self.board = copy.deepcopy(board)

    def provide_board(self):
        return self.board

    def put_stone(self, x, y):
        # PutStone @ CanPutStone IsTrue
        if self.can_put_stone(x, y):
            if self.can_reverse(x, y, 0, -1):
                self.reverse_stone(x, y, 0, -1)

            if self.can_reverse(x, y, 0, 1):
                self.reverse_stone(x, y, 0, 1)

            if self.can_reverse(x, y, -1, 0):
                self.reverse_stone(x, y, -1, 0)

            if self.can_reverse(x, y, 1, 0):
                self.reverse_stone(x, y, 1, 0)

            if self.can_reverse(x, y, -1, -1):
                self.reverse_stone(x, y, -1, -1)

            if self.can_reverse(x, y, 1, -1):
                self.reverse_stone(x, y, 1, -1)

            if self.can_reverse(x, y, -1, 1):
                self.reverse_stone(x, y, -1, 1)

            if self.can_reverse(x, y, 1, 1):
                self.reverse_stone(x, y, 1, 1)

            return True
        else:
            return False

    def reverse_stone(self, x, y, dx, dy):
        ref_x = x
        ref_y = y

        while True:
            self.board[ref_y][ref_x] = self.color
            ref_x += dx
            ref_y += dy

            if self.board[ref_y][ref_x] == self.color:
                break

    def can_put_stone(self, x, y):
        # check you can put stone at point(x, y)
        if self.is_none(x, y):
            up = self.can_reverse(x, y, 0, -1)
            down = self.can_reverse(x, y, 0, 1)
            left = self.can_reverse(x, y, -1, 0)
            right = self.can_reverse(x, y, 1, 0)
            up_left = self.can_reverse(x, y, -1, -1)
            up_right = self.can_reverse(x, y, 1, -1)
            down_left = self.can_reverse(x, y, -1, 1)
            down_right = self.can_reverse(x, y, 1, 1)

            return up or down or left or right or up_left or up_right or down_left or down_right
        else:
            return False

    def is_none(self, x, y):
        # check board at point(x, y) is none
        if self.board[y][x] == NONE:
            return True
        else:
            return False

    def can_reverse(self, x, y, dx, dy):
        # check you can reverse stone if you put at point(x, y)
        ref_x = x + dx
        ref_y = y + dy

        if ref_x < 0 or BOARD_SIZE <= ref_x or ref_y < 0 or BOARD_SIZE <= ref_y:
            return False
        elif self.board[ref_y][ref_x] == NONE or self.board[ref_y][ref_x] == self.color:
            return False
        else:
            ref_x += dx
            ref_y += dy

            while 0 <= ref_x < BOARD_SIZE and 0 <= ref_y < BOARD_SIZE:
                if self.board[ref_y][ref_x] == self.color:
                    return True
                elif self.board[ref_y][ref_x] == NONE:
                    return False
                else:
                    ref_x += dx
                    ref_y += dy

            return False


class CpuPlayer(Player):
    color = BLACK
    board = []

    def __init__(self, color):
        self.color = color

    def put_stone(self):
        while True:
            x = random.randrange(BOARD_SIZE)
            y = random.randrange(BOARD_SIZE)
            if super().put_stone(x, y):
                break


class Othello:
    board = []
    player_1 = CpuPlayer(BLACK)
    player_2 = CpuPlayer(WHITE)

    def __init__(self):
        # Constructor
        # Init Board and Run Othello
        self.board = [[NONE for i in range((BOARD_SIZE))] for j in range(BOARD_SIZE)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE

    def draw_board(self):
        # Draw Board
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == BLACK:
                    print(" ○ ", end="")
                elif self.board[i][j] == WHITE:
                    print(" ● ", end="")
                else:
                    print(" * ", end="")
            print()

    def can_put(self, player: Player):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if player.can_put_stone(j, i):
                    return True
                else:
                    continue
        return False

    def input(self, player: Player):
        while True:
            print("Input Your Put")
            print("x y -> ", end="")
            x, y = [int(i) for i in input().split()]
            x -= 1
            y -= 1

            if player.put_stone(x, y):
                self.board = copy.deepcopy(player.provide_board())
                break
            else:
                print("Sorry")

    def running(self):
        while True:
            # Player-1 Move
            self.draw_board()
            self.player_1.get_board(self.board)
            p1_can_put = self.can_put(self.player_1)
            if p1_can_put:  # Pass Check
                # self.input(self.player_1)
                self.player_1.put_stone()
                self.board = copy.deepcopy(self.player_1.provide_board())
            else:
                print("Player-1 is Pass")

            print()

            # Player-2 Move
            self.draw_board()
            self.player_2.get_board(self.board)
            p2_can_put = self.can_put(self.player_2)
            if p2_can_put:  # Pass Check
                # self.input(self.player_2)
                self.player_2.put_stone()
                self.board = copy.deepcopy(self.player_2.provide_board())
            else:
                print("Player-2 is Pass")

            print()  # \n

            if p1_can_put is False and p2_can_put is False:
                break

        self.game_result()

    def game_result(self):
        count_p1 = 0
        count_p2 = 0

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == self.player_1.color:
                    count_p1 += 1
                elif self.board[i][j] == self.player_2.color:
                    count_p2 += 1

        if self.player_1.color == BLACK:
            stone_p1 = "◯"
            stone_p2 = "●"
        else:
            stone_p1 = "●"
            stone_p2 = "◯"

        if count_p1 > count_p2:
            result_p1 = "WIN"
            result_p2 = ""
        elif count_p1 < count_p2:
            result_p1 = ""
            result_p2 = "WIN"
        else:
            result_p1 = ""
            result_p2 = ""

        print("Player-1: %s%d %s" % (stone_p1, count_p1, result_p1))
        print("Player-2: %s%d %s" % (stone_p2, count_p2, result_p2))


run = Othello()
run.running()
