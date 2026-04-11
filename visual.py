import pygame

from stone_enum import OccupyStatus
from common.const import BOARD_WIDTH, BOARD_HEIGHT
from common.const import UNIT, MID_UNIT
from common.const import LINE_NUM, LINE_WIDTH, STONE_INNER_RADIUS, STONE_OUTER_RADIUS
from common.const import SQUARE_WIDTH, SQUARE_INDEX
from common.const import STAR_POINT_LIST
from common.color import WOOD, BLACK, BURGUNDY, WHITE
from common.color import MILD_BLACK, MILD_WHITE, MILD_BURGUNDY

from sgf_process import sgf_read


class Visual:
    def __init__(self):
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

    def opening_display(self, board_info: list[list[OccupyStatus]], last_move: list[int]):
        self.draw_board(MILD_BLACK)
        self.draw_stones(board_info, MILD_BURGUNDY, MILD_WHITE)

        if last_move[0] >= 0 and last_move[1] >= 0:
            self.last_move_hint(board_info, last_move, MILD_WHITE, MILD_BLACK)
        pygame.display.update()

    def self_play_display(self, board_info: list[list[OccupyStatus]], last_move: list[int]):
        self.draw_board()
        self.draw_stones(board_info)
        self.last_move_hint(board_info, last_move)
        self.mouse_hint(board_info, last_move)
        pygame.display.update()

    def draw_board(self, line_color=BLACK):
        self.screen.fill(WOOD)
        for i in range(LINE_NUM):
            pygame.draw.line(self.screen, line_color,
                             (MID_UNIT + UNIT, MID_UNIT + (i + 1) * UNIT),
                             (MID_UNIT + 19 * UNIT, MID_UNIT + (i + 1) * UNIT),
                             LINE_WIDTH)
            pygame.draw.line(self.screen, line_color,
                             (MID_UNIT + (i + 1) * UNIT, MID_UNIT + UNIT),
                             (MID_UNIT + (i + 1) * UNIT, MID_UNIT + 19 * UNIT),
                             LINE_WIDTH)

        for i in range(len(STAR_POINT_LIST)):
            pygame.draw.circle(self.screen, line_color,
                               (STAR_POINT_LIST[i][0] * UNIT + MID_UNIT + 1,
                                STAR_POINT_LIST[i][1] * UNIT + MID_UNIT + 1),
                               4 * LINE_WIDTH)

    def draw_stones(self, board_info: list[list[OccupyStatus]],
                    black_stone_color=BURGUNDY, white_stone_color=WHITE):
        # TODO: catch index out of range exception
        for i in range(LINE_NUM):
            for j in range(LINE_NUM):
                if board_info[i][j] == OccupyStatus.Black:
                    self.set_black_stone(i, j, black_stone_color)
                elif board_info[i][j] == OccupyStatus.White:
                    self.set_white_stone(i, j, black_stone_color, white_stone_color)

    def last_move_hint(self, board_info: list[list[OccupyStatus]], last_move: list[int],
                       black_move_color=WHITE, white_move_color=BLACK):
        if last_move[0] == -1:
            return
        if board_info[last_move[0]][last_move[1]] == OccupyStatus.Black:
            self.set_dot(last_move[0], last_move[1], black_move_color)
        elif board_info[last_move[0]][last_move[1]] == OccupyStatus.White:
            self.set_dot(last_move[0], last_move[1], white_move_color)
        else:
            # TODO: throw exception
            pass

    def mouse_hint(self, board_info: list[list[OccupyStatus]], last_move: list[int]):
        x, y = pygame.mouse.get_pos()
        x_num = x // UNIT - 1
        y_num = y // UNIT - 1
        if 0 <= x_num <= 18 and 0 <= y_num <= 18:
            if board_info[x_num][y_num] == OccupyStatus.Free:
                if last_move[0] == -1:
                    self.set_black_square(x_num, y_num)
                elif board_info[last_move[0]][last_move[1]] == OccupyStatus.Black:
                    self.set_white_square(x_num, y_num)
                elif board_info[last_move[0]][last_move[1]] == OccupyStatus.White:
                    self.set_black_square(x_num, y_num)
                else:
                    # TODO: throw exception
                    pass

    def set_black_stone(self, x: int, y: int, stone_color=BURGUNDY):
        pygame.draw.circle(self.screen, stone_color,
                           ((x + 1) * UNIT + MID_UNIT + 1,
                            (y + 1) * UNIT + MID_UNIT + 1),
                           STONE_OUTER_RADIUS)

    def set_white_stone(self, x: int, y: int, outer_color=BURGUNDY, inner_color=WHITE):
        self.set_black_stone(x, y, outer_color)
        pygame.draw.circle(self.screen, inner_color,
                           ((x + 1) * UNIT + MID_UNIT + 1,
                            (y + 1) * UNIT + MID_UNIT + 1),
                           STONE_INNER_RADIUS)

    def set_black_square(self, x: int, y: int):
        rect = ((x + 1) * UNIT + SQUARE_INDEX, (y + 1) * UNIT + SQUARE_INDEX,
                SQUARE_WIDTH, SQUARE_WIDTH)
        pygame.draw.rect(self.screen, BURGUNDY, rect)

    def set_white_square(self, x: int, y: int):
        rect = ((x + 1) * UNIT + SQUARE_INDEX, (y + 1) * UNIT + SQUARE_INDEX,
                SQUARE_WIDTH, SQUARE_WIDTH)
        pygame.draw.rect(self.screen, WHITE, rect)

    def set_dot(self, x: int, y: int, dot_color):
        pygame.draw.circle(self.screen, dot_color,
                           ((x + 1) * UNIT + MID_UNIT + 1,
                            (y + 1) * UNIT + MID_UNIT + 1),
                           STONE_INNER_RADIUS // 2)
