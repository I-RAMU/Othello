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
    tmp_board = []
    put_count = 0

    board_weight_1 = [
        [120, -20, 20, 5, 5, 20, -20, 120],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [20, -5, 15, 3, 3, 15, -5, -5, 20],
        [5, -5, 3, 3, 3, 3, -5, 5],
        [5, -5, 3, 3, 3, 3, -5, 5],
        [20, -5, 15, 3, 3, 15, -5, -5, 20],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [120, -20, 20, 5, 5, 20, -20, 120]
    ]
    board_weight_2 = [
        [30, -12, 0, -1, -1, 0, -12, 30],
        [-12, -15, -3, -3, -3, -3, -15, -12],
        [0, -3, 0, -1, -1, 0, -3, 0],
        [-1, -3, -1, -1, -1, -1, -3, -1],
        [-1, -3, -1, -1, -1, -1, -3, -1],
        [0, -3, 0, -1, -1, 0, -3, 0],
        [-12, -15, -3, -3, -3, -3, -15, -12],
        [30, -12, 0, -1, -1, 0, -12, 30]
    ]

    def __init__(self, color):
        self.color = color

    def put_stone(self):
        self.tmp_board = copy.deepcopy(self.board)
        self.put_count += 1
        eval_value = -255
        ret_x = -1
        ret_y = -1

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if super().put_stone(j, i):
                    score_tmp = self.eval_board()

                    if eval_value < score_tmp:
                        ret_x = j
                        ret_y = i
                        eval_value = score_tmp

                    self.board = copy.deepcopy(self.tmp_board)

        self.board = copy.deepcopy(self.tmp_board)
        super().put_stone(ret_x, ret_y)
        print("CPU Put @ (%d, %d)" % (ret_x + 1, ret_y + 1))

    def eval_board(self):
        score_black = 0
        score_white = 0

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == NONE:
                    continue
                elif self.board[i][j] == BLACK:
                    if self.put_count <= 5:
                        score_black += self.board_weight_1[i][j]
                    else:
                        score_black += self.board_weight_2[i][j]
                else:
                    if self.put_count <= 5:
                        score_white += self.board_weight_1[i][j]
                    else:
                        score_white += self.board_weight_2[i][j]

        if self.color == BLACK:
            return score_black - score_white
        else:
            return score_white - score_black


class Othello:
    board = []
    player_1 = CpuPlayer(BLACK)
    player_2 = CpuPlayer(WHITE)
    mode = 3

    def __init__(self):
        # Constructor
        # Init Board and Run Othello
        self.board = [[NONE for i in range((BOARD_SIZE))] for j in range(BOARD_SIZE)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE

        self.select_mode()

        if self.mode == 1:
            self.player_1 = Player(BLACK)
            self.player_2 = Player(WHITE)
        elif self.mode == 2:
            self.player_1 = Player(BLACK)
            self.player_2 = CpuPlayer(WHITE)
        else:
            self.player_1 = CpuPlayer(BLACK)
            self.player_2 = CpuPlayer(WHITE)

    def select_mode(self):
        print("--------------------------")
        print("Select Game Mode!")
        print("1 : Player vs Player")
        print("2 : Player vs CPU")
        print("3 : CPU vs CPU")

        while True:
            print("Input -> ", end="")

            try:
                self.mode = int(input())
            except ValueError:
                continue
            else:
                if 0 < self.mode < 4:
                    break
                else:
                    continue

        print("--------------------------")

    def draw_board(self):
        # Draw Board
        print("y\\x", end="")
        for i in range(BOARD_SIZE):
            print(" %d " % (i+1), end="")

        print()

        for i in range(BOARD_SIZE):
            print("% d" % (i+1), end=" ")
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
        if type(player) is CpuPlayer:
            player.put_stone()
            self.board = copy.deepcopy(player.provide_board())
        else:
            while True:
                print("Input Your Put")
                print("x y -> ", end="")
                try:
                    x, y = [int(i) for i in input().split()]
                    x -= 1
                    y -= 1
                except ValueError:
                    continue
                else:
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                        if player.put_stone(x, y):
                            self.board = copy.deepcopy(player.provide_board())
                            break
                        else:
                            print("Sorry")
                    else:
                        continue

    def running(self):
        while True:
            # Pass Check
            self.player_1.get_board(self.board)
            self.player_2.get_board(self.board)
            if self.can_put(self.player_1) is False and self.can_put(self.player_2) is False:
                print("\n")
                self.draw_board()
                print("Game End!")
                break

            # Player-1 Move
            self.draw_board()
            self.player_1.get_board(self.board)
            p1_can_put = self.can_put(self.player_1)
            if p1_can_put:  # Pass Check
                self.input(self.player_1)
            else:
                print("Player-1 is Pass")

            print()

            # Player-2 Move
            self.draw_board()
            self.player_2.get_board(self.board)
            p2_can_put = self.can_put(self.player_2)
            if p2_can_put:  # Pass Check
                self.input(self.player_2)
            else:
                print("Player-2 is Pass")

            print()  # \n

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
