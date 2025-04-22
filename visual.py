import pygame

from stone_enum import OccupyStatus
from common.const import BOARD_WIDTH, BOARD_HEIGHT
from common.const import UNIT, MID_UNIT
from common.const import LINE_NUM, LINE_WIDTH, STONE_INNER_RADIUS, STONE_OUTER_RADIUS
from common.const import SQUARE_WIDTH, SQUARE_INDEX
from common.const import STAR_POINT_LIST
from common.color import WOOD, BLACK, BURGUNDY, WHITE


class Visual:
    def __init__(self):
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

    def display(self, board_info: list[list[OccupyStatus]], last_move: list[int]):
        self.draw_board()
        self.draw_stones(board_info)
        self.last_move_hint(board_info, last_move)
        self.mouse_hint(board_info, last_move)
        pygame.display.update()

    def draw_board(self):
        self.screen.fill(WOOD)
        for i in range(LINE_NUM):
            pygame.draw.line(self.screen, BLACK,
                             (MID_UNIT + UNIT, MID_UNIT + (i + 1) * UNIT),
                             (MID_UNIT + 19 * UNIT, MID_UNIT + (i + 1) * UNIT),
                             LINE_WIDTH)
            pygame.draw.line(self.screen, BLACK,
                             (MID_UNIT + (i + 1) * UNIT, MID_UNIT + UNIT),
                             (MID_UNIT + (i + 1) * UNIT, MID_UNIT + 19 * UNIT),
                             LINE_WIDTH)

        for i in range(len(STAR_POINT_LIST)):
            pygame.draw.circle(self.screen, BLACK,
                               (STAR_POINT_LIST[i][0] * UNIT + MID_UNIT + 1,
                                STAR_POINT_LIST[i][1] * UNIT + MID_UNIT + 1),
                               4 * LINE_WIDTH)

    def draw_stones(self, board_info: list[list[OccupyStatus]]):
        # TODO: catch index out of range exception
        for i in range(LINE_NUM):
            for j in range(LINE_NUM):
                if board_info[i][j] == OccupyStatus.Black:
                    self.set_black_stone(i, j)
                elif board_info[i][j] == OccupyStatus.White:
                    self.set_white_stone(i, j)

    def last_move_hint(self, board_info: list[list[OccupyStatus]], last_move: list[int]):
        if last_move[0] == -1:
            return
        if board_info[last_move[0]][last_move[1]] == OccupyStatus.Black:
            self.set_white_dot(last_move[0], last_move[1])
        elif board_info[last_move[0]][last_move[1]] == OccupyStatus.White:
            self.set_black_dot(last_move[0], last_move[1])
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

    def set_black_stone(self, x: int, y: int):
        pygame.draw.circle(self.screen, BURGUNDY,
                           ((x + 1) * UNIT + MID_UNIT + 1,
                            (y + 1) * UNIT + MID_UNIT + 1),
                           STONE_OUTER_RADIUS)

    def set_white_stone(self, x: int, y: int):
        self.set_black_stone(x, y)
        pygame.draw.circle(self.screen, WHITE,
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

    def set_black_dot(self, x: int, y: int):
        pygame.draw.circle(self.screen, BURGUNDY,
                           ((x + 1) * UNIT + MID_UNIT + 1,
                            (y + 1) * UNIT + MID_UNIT + 1),
                           STONE_INNER_RADIUS // 2)

    def set_white_dot(self, x: int, y: int):
        pygame.draw.circle(self.screen, WHITE,
                           ((x + 1) * UNIT + MID_UNIT + 1,
                            (y + 1) * UNIT + MID_UNIT + 1),
                           STONE_INNER_RADIUS // 2)
