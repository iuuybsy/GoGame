import pygame
import ctypes
import colors
import sys


user32 = ctypes.windll.user32
SCREEN_WIDTH: int = user32.GetSystemMetrics(0)
SCREEN_HEIGHT: int = user32.GetSystemMetrics(1)

UNIT: int = (SCREEN_HEIGHT // 10 * 9) // 21
if UNIT % 2 == 0:
    UNIT += 1
MID_UNIT = UNIT // 2 + 1

BOARD_HEIGHT_UNIT_NUM: int = 21
BOARD_WIDTH_UNIT_NUM: int = 27

BOARD_WIDTH: int = BOARD_WIDTH_UNIT_NUM * UNIT
BOARD_HEIGHT: int = BOARD_HEIGHT_UNIT_NUM * UNIT

LINE_WIDTH: int = int(UNIT * 0.05)
LINE_NUM = 19

STAR_POINT_LIST = [[4, 4], [4, 16], [16, 4], [16, 16],
                   [4, 10], [10, 4], [16, 10], [10, 16],
                   [10, 10]]

STONE_OUTER_RADIUS: int = MID_UNIT - 1
STONE_INNER_RADIUS: int = int(STONE_OUTER_RADIUS * 0.8)


class GameBoard:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(colors.GREY)
            # self.screen_block_check()
            self.draw_board()
            for i in range(10):
                for j in range(10):
                    if (i + j) % 2 == 0:
                        self.set_black_stone(i, j)
                    else:
                        self.set_white_stone(i, j)
            for i in range(11, 19):
                for j in range(11, 19):
                    if i % 2 == 0:
                        self.set_black_stone(i, j)
                    else:
                        self.set_white_stone(i, j)
            pygame.display.flip()

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







