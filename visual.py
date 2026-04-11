import pygame
import math

from stone_enum import OccupyStatus
from common.const import BOARD_WIDTH, BOARD_HEIGHT
from common.const import UNIT, MID_UNIT
from common.const import LINE_NUM, LINE_WIDTH, STONE_INNER_RADIUS, STONE_OUTER_RADIUS
from common.const import OPTION_OUTER_RADIUS, OPTION_INNER_RADIUS
from common.const import SQUARE_WIDTH, SQUARE_INDEX
from common.const import STAR_POINT_LIST
from common.const import OPENING_OPTION_BLACK_POS, OPENING_OPTION_WHITE_POS, OPENING_OPTION_RANDOM_POS

from common.color import WOOD, BLACK, BURGUNDY, WHITE
from common.color import MILD_BLACK, MILD_WHITE, MILD_BURGUNDY

from sgf_process import sgf_read


class Visual:
    def __init__(self):
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

    def opening_display(self, board_info: list[list[OccupyStatus]], last_move: list[int],
                        point_to_black, point_to_white, point_to_random):
        self.draw_board(MILD_BLACK)
        self.draw_stones(board_info, MILD_BURGUNDY, MILD_WHITE)

        if last_move[0] >= 0 and last_move[1] >= 0:
            self.last_move_hint(board_info, last_move, MILD_WHITE, MILD_BURGUNDY)

        self.opening_choose_color_option(point_to_black, point_to_white, point_to_random)

        pygame.display.update()

    def opening_choose_color_icon(self):
        self.set_black_stone(OPENING_OPTION_BLACK_POS[0], OPENING_OPTION_BLACK_POS[1])
        self.set_white_stone(OPENING_OPTION_WHITE_POS[0], OPENING_OPTION_WHITE_POS[1])
        self.draw_random_stone(OPENING_OPTION_RANDOM_POS[0], OPENING_OPTION_RANDOM_POS[1])

    def opening_choose_color_option(self, point_to_black, point_to_white, point_to_random):
        if point_to_black:
            self.draw_option_circle(OPENING_OPTION_BLACK_POS[0], OPENING_OPTION_BLACK_POS[1])
        elif point_to_white:
            self.draw_option_circle(OPENING_OPTION_WHITE_POS[0], OPENING_OPTION_WHITE_POS[1])
        elif point_to_random:
            self.draw_option_circle(OPENING_OPTION_RANDOM_POS[0], OPENING_OPTION_RANDOM_POS[1])
        self.opening_choose_color_icon()

    def self_play_display(self, board_info: list[list[OccupyStatus]], last_move: list[int], point_to_reset: bool):
        self.draw_board()
        self.draw_stones(board_info)
        self.last_move_hint(board_info, last_move)
        self.mouse_hint(board_info, last_move)
        reset_option_color = BURGUNDY if point_to_reset else MILD_BURGUNDY
        self.draw_restart_stone_left_arrow(9, 20, reset_option_color)
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
                       black_move_color=WHITE, white_move_color=BURGUNDY):
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

    def draw_random_stone(self, x: int, y: int, outer_color=MILD_BURGUNDY):
        cx = (x + 1) * UNIT + MID_UNIT + 1
        cy = (y + 1) * UNIT + MID_UNIT + 1
        r_outer = STONE_OUTER_RADIUS
        r_inner = STONE_INNER_RADIUS

        pygame.draw.circle(self.screen, outer_color, (cx, cy), r_outer)

        left_rect = (cx - r_inner, cy - r_inner, r_inner, 2 * r_inner)
        pygame.draw.ellipse(self.screen, BURGUNDY, left_rect)

        right_rect = (cx, cy - r_inner, r_inner, 2 * r_inner)
        pygame.draw.ellipse(self.screen, WHITE, right_rect)

        eye_radius = r_inner // 5
        pygame.draw.circle(self.screen, WHITE, (cx - r_inner//2, cy - r_inner//2), eye_radius)
        pygame.draw.circle(self.screen, BURGUNDY, (cx + r_inner//2, cy + r_inner//2), eye_radius)

    def draw_option_circle(self, x: int, y: int, outer_color=BURGUNDY, inner_color=WOOD):
        pygame.draw.circle(self.screen, outer_color,
                           ((x + 1) * UNIT + MID_UNIT + 1,
                            (y + 1) * UNIT + MID_UNIT + 1),
                           OPTION_OUTER_RADIUS)
        pygame.draw.circle(self.screen, inner_color,
                           ((x + 1) * UNIT + MID_UNIT + 1,
                            (y + 1) * UNIT + MID_UNIT + 1),
                           OPTION_INNER_RADIUS)


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

    def draw_restart_stone_left_arrow(self, x: int, y: int,
                                      color=MILD_BURGUNDY):
        cx = (x + 1) * UNIT + MID_UNIT + 1
        cy = (y + 1) * UNIT + MID_UNIT + 1
        r_inner = OPTION_INNER_RADIUS

        pygame.draw.circle(self.screen, color, (cx, cy), OPTION_OUTER_RADIUS)
        pygame.draw.circle(self.screen, WOOD, (cx, cy), OPTION_INNER_RADIUS)

        arrow_width = r_inner * 0.7
        arrow_thick = max(3, int(r_inner * 0.25))
        head_len = r_inner * 0.45
        head_width = r_inner * 0.55

        shaft_left_x = cx - arrow_width / 2

        shaft_rect = pygame.Rect(shaft_left_x, cy - arrow_thick / 2,
                                 arrow_width + 10, arrow_thick)
        pygame.draw.rect(self.screen, color, shaft_rect)

        tip_x = shaft_left_x - 10
        tip_y = cy
        top_x = shaft_left_x + head_len
        top_y = cy - head_width / 2
        bottom_x = shaft_left_x + head_len
        bottom_y = cy + head_width / 2

        pygame.draw.polygon(self.screen, color,
                            [(tip_x, tip_y), (top_x, top_y), (bottom_x, bottom_y)])
