import pygame
import ctypes
import colors
import sys
import time
import copy
from core_logic import CoreLogic
from stones import OccupyStatus

user32 = ctypes.windll.user32
SCREEN_WIDTH: int = user32.GetSystemMetrics(0)
SCREEN_HEIGHT: int = user32.GetSystemMetrics(1)

UNIT: int = 41
MID_UNIT = UNIT // 2 + 1

SQUARE_WIDTH = int(UNIT * 0.4)
if SQUARE_WIDTH % 2 == 0:
    SQUARE_WIDTH += 1
SQUARE_INDEX = int((UNIT - SQUARE_WIDTH) * 0.5) + 1

BOARD_HEIGHT_UNIT_NUM: int = 21
BOARD_WIDTH_UNIT_NUM: int = 21

BOARD_WIDTH: int = BOARD_WIDTH_UNIT_NUM * UNIT
BOARD_HEIGHT: int = BOARD_HEIGHT_UNIT_NUM * UNIT

LINE_WIDTH: int = int(UNIT * 0.05)
LINE_NUM = 19

STAR_POINT_LIST = [[4, 4], [4, 16], [16, 4], [16, 16],
                   [4, 10], [10, 4], [16, 10], [10, 16],
                   [10, 10]]

STONE_OUTER_RADIUS: int = MID_UNIT - 1
STONE_INNER_RADIUS: int = int(STONE_OUTER_RADIUS * 0.8)

MIN_MOVE_TIME = 300.0


class GameBoard:
    def __init__(self):
        pygame.init()
        self.logic = CoreLogic()
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        self.moves = []
        self.last_move_time = time.time()

    def self_play(self):
        last_stone = [-1, -1]
        while True:
            self.screen.fill(colors.GREY)
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            x, y = pygame.mouse.get_pos()
            x_num = x // UNIT - 1
            y_num = y // UNIT - 1
            if 0 <= x_num <= 18 and 0 <= y_num <= 18:
                if x_num != self.logic.ko[0] or y_num != self.logic.ko[1]:
                    if not self.logic.is_occupied_by_stone(x_num, y_num):
                        if self.logic.black_turn:
                            self.set_black_square(x_num, y_num)
                        else:
                            self.set_white_square(x_num, y_num)
                    left, _, right = pygame.mouse.get_pressed()
                    delta_time = (time.time() - self.last_move_time) * 1000.0
                    if delta_time > MIN_MOVE_TIME:
                        if not self.logic.is_occupied_by_stone(x_num, y_num):
                            if left:
                                self.logic.set_stone(x_num, y_num)
                                if self.logic.valid:
                                    last_stone[0] = x_num
                                    last_stone[1] = y_num
                                    self.moves.append(copy.deepcopy(last_stone))
                                    self.last_move_time = time.time()
                            elif right:
                                self.logic.regret()
                                last_stone[0] = -1
                                last_stone[1] = -1
                                if len(self.moves) > 1:
                                    last_stone[0] = self.moves[-2][0]
                                    last_stone[1] = self.moves[-2][1]
                                    self.moves.pop()
                                self.last_move_time = time.time()
            for j in range(19):
                for k in range(19):
                    if self.logic.board_info[j][k] == OccupyStatus.Black:
                        self.set_black_stone(j, k)
                    if self.logic.board_info[j][k] == OccupyStatus.White:
                        self.set_white_stone(j, k)
            if last_stone[0] >= 0 and last_stone[1] >= 0:
                self.set_red_dot(last_stone[0], last_stone[1])
            pygame.display.flip()

    def logic_test(self, adv_black: list, adv_white: list, moves: list, black_first: bool):
        if len(adv_black) > 0:
            for i in range(len(adv_black)):
                x, y = adv_black[i]
                if not self.logic.black_turn:
                    self.logic.pass_this_move()
                self.logic.set_stone(x, y)
        if len(adv_white) > 0:
            for i in range(len(adv_white)):
                x, y = adv_white[i]
                if self.logic.black_turn:
                    self.logic.pass_this_move()
                self.logic.set_stone(x, y)
        if not black_first:
            self.logic.pass_this_move()
        for i in range(len(moves)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            x, y = moves[i]
            self.logic.set_stone(x, y)
            self.screen.fill(colors.GREY)
            # self.screen_block_check()
            self.draw_board()
            for j in range(19):
                for k in range(19):
                    if self.logic.board_info[j][k] == OccupyStatus.Black:
                        self.set_black_stone(j, k)
                    if self.logic.board_info[j][k] == OccupyStatus.White:
                        self.set_white_stone(j, k)
            self.set_red_dot(x, y)
            pygame.display.flip()
            time.sleep(0.5)

    def screen_block_check(self):
        for i in range(BOARD_WIDTH_UNIT_NUM):
            for j in range(BOARD_HEIGHT_UNIT_NUM):
                left = i * UNIT + LINE_WIDTH
                top = j * UNIT + LINE_WIDTH
                width = UNIT - 2 * LINE_WIDTH
                height = UNIT - 2 * LINE_WIDTH
                rect = (left, top, width, height)
                pygame.draw.rect(self.screen, colors.WHITE, rect, 0)

    def draw_board(self):
        for i in range(LINE_NUM):
            pygame.draw.line(self.screen, colors.BLACK,
                             (MID_UNIT + UNIT, MID_UNIT + (i + 1) * UNIT),
                             (MID_UNIT + 19 * UNIT, MID_UNIT + (i + 1) * UNIT),
                             LINE_WIDTH)
            pygame.draw.line(self.screen, colors.BLACK,
                             (MID_UNIT + (i + 1) * UNIT, MID_UNIT + UNIT),
                             (MID_UNIT + (i + 1) * UNIT, MID_UNIT + 19 * UNIT),
                             LINE_WIDTH)

        for i in range(len(STAR_POINT_LIST)):
            pygame.draw.circle(self.screen, colors.BLACK,
                               (STAR_POINT_LIST[i][0] * UNIT + MID_UNIT + 1,
                                STAR_POINT_LIST[i][1] * UNIT + MID_UNIT + 1),
                               4 * LINE_WIDTH)

    def set_black_stone(self, x: int, y: int):
        pygame.draw.circle(self.screen, colors.BLACK,
                           ((x + 1) * UNIT + MID_UNIT + 1,
                            (y + 1) * UNIT + MID_UNIT + 1),
                           STONE_OUTER_RADIUS)

    def set_white_stone(self, x: int, y: int):
        self.set_black_stone(x, y)
        pygame.draw.circle(self.screen, colors.WHITE,
                           ((x + 1) * UNIT + MID_UNIT + 1,
                            (y + 1) * UNIT + MID_UNIT + 1),
                           STONE_INNER_RADIUS)

    def set_black_square(self, x: int, y: int):
        rect = ((x + 1) * UNIT + SQUARE_INDEX, (y + 1) * UNIT + SQUARE_INDEX,
                SQUARE_WIDTH, SQUARE_WIDTH)
        pygame.draw.rect(self.screen, colors.BLACK, rect)

    def set_white_square(self, x: int, y: int):
        rect = ((x + 1) * UNIT + SQUARE_INDEX, (y + 1) * UNIT + SQUARE_INDEX,
                SQUARE_WIDTH, SQUARE_WIDTH)
        pygame.draw.rect(self.screen, colors.WHITE, rect)

    def set_red_dot(self, x: int, y: int):
        pygame.draw.circle(self.screen, colors.RED,
                           ((x + 1) * UNIT + MID_UNIT + 1,
                            (y + 1) * UNIT + MID_UNIT + 1),
                           STONE_INNER_RADIUS // 2)
