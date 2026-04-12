import pygame
import sys
import time
import random
import os
import math
import subprocess

from enum import Enum

from common import MID_UNIT
from visual import Visual
from go_logic import GoLogic
from common.const import UNIT, DELTA_TIME
from common.const import OPENING_OPTION_BLACK_POS, OPENING_OPTION_WHITE_POS, OPENING_OPTION_RANDOM_POS
from common.const import RESET_POS_X_RANGE
from common.const import OPTION_OUTER_RADIUS

from common.path import KATAGO_PATH, CONFIG_PATH, MODEL_PATH

from sgf_process import sgf_read


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def gtp_to_coord(gtp_str: str, board_size: int = 19) -> list[int]:

    gtp = gtp_str.strip().upper()
    if gtp in ("PASS", "RESIGN"):
        return [-1, -1]

    if len(gtp) < 2 or not gtp[0].isalpha() or not gtp[1:].isdigit():
        raise ValueError(f"Invalid GTP cord: '{gtp_str}'")

    col_letter = gtp[0]
    row_str = gtp[1:]

    # 列字母转换（跳过 'I'）
    if col_letter < 'A' or col_letter > 'T' or col_letter == 'I':
        raise ValueError(f"Invalid letter: '{col_letter}'")
    col = ord(col_letter) - ord('A')
    if col_letter > 'I':
        col -= 1

    # 行号转换：GTP 行号 1 为棋盘底边，映射到我们的坐标系（行索引从 0 顶边开始）
    gtp_row = int(row_str)
    if not (1 <= gtp_row <= board_size):
        raise ValueError(f"'{gtp_row}' out of range")
    row = board_size - gtp_row   # 上下翻转

    if not (0 <= col < board_size):
        raise ValueError(f"cord '{gtp_str}' out of range")

    return [col, row]


def coord_to_gtp(coord: list[int], board_size: int = 19) -> str:
    if not isinstance(coord, (list, tuple)) or len(coord) != 2:
        raise ValueError("Invalid coordinate format")

    col, row = coord
    if row == -1 and col == -1:
        return "PASS"

    if not (0 <= row < board_size and 0 <= col < board_size):
        raise ValueError(f"cord [{row}, {col}] out of range")

    gtp_row = board_size - row

    if col >= 8:
        col_letter = chr(ord('A') + col + 1)
    else:
        col_letter = chr(ord('A') + col)

    return f"{col_letter}{gtp_row}"


class GoGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.stone_sounds = [
            pygame.mixer.Sound(resource_path("sounds/stone1.wav")),
            pygame.mixer.Sound(resource_path("sounds/stone2.wav")),
            pygame.mixer.Sound(resource_path("sounds/stone3.wav")),
            pygame.mixer.Sound(resource_path("sounds/stone4.wav")),
            pygame.mixer.Sound(resource_path("sounds/stone5.wav"))
        ]
        for sound in self.stone_sounds:
            sound.set_volume(1.0)
        self.process = subprocess.Popen([KATAGO_PATH, 'gtp',
                            '-model', MODEL_PATH,
                            '-config', CONFIG_PATH],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, bufsize=1)
        self.go_logic = GoLogic()
        self.visual = Visual()
        self.last_move_time = time.time()

    @staticmethod
    def get_mouse_pos_num() -> tuple[int, int]:
        x, y = pygame.mouse.get_pos()
        x_num = x // UNIT - 1
        y_num = y // UNIT - 1
        return x_num, y_num

    def opening_option_judgement(self) -> tuple[bool, bool, bool]:
        x_num, y_num = self.get_mouse_pos_num()
        point_to_black = x_num == OPENING_OPTION_BLACK_POS[0] and y_num == OPENING_OPTION_BLACK_POS[1]
        point_to_white = x_num == OPENING_OPTION_WHITE_POS[0] and y_num == OPENING_OPTION_WHITE_POS[1]
        point_to_random = x_num == OPENING_OPTION_RANDOM_POS[0] and y_num == OPENING_OPTION_RANDOM_POS[1]
        return point_to_black, point_to_white, point_to_random

    def opening(self) -> tuple[bool, bool, bool]:
        moves = sgf_read("opening.sgf")
        last_move_time = time.time()
        ind = 0
        pygame.event.clear()
        while True:
            point_to_black, point_to_white, point_to_random = self.opening_option_judgement()
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.katago_terminate()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and (point_to_black or point_to_white or point_to_random):
                        mouse_clicked = True
            if mouse_clicked:
                break
            last_move = self.go_logic.last_move
            if ind >= len(moves):
                last_move = [-1, -1]
            self.visual.opening_display(self.go_logic.board_info, last_move,
                                        point_to_black, point_to_white, point_to_random)
            if ind < len(moves):
                x_num, y_num = moves[ind]
                self.go_logic.set_stone(x_num, y_num)
                if time.time() - last_move_time > 1:
                    ind += 1
                    last_move_time = time.time()
        return point_to_black, point_to_white, point_to_random

    def self_play(self):
        while True:
            self.visual.self_play_display(self.go_logic.board_info, self.go_logic.last_move)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.katago_terminate()
                    sys.exit()

            x_num, y_num = self.get_mouse_pos_num()
            if 0 <= x_num <= 18 and 0 <= y_num <= 18:
                left, _, right = pygame.mouse.get_pressed()
                current_time = time.time()
                if left and current_time - self.last_move_time > DELTA_TIME:
                    if self.go_logic.set_stone(x_num, y_num):
                        self.stone_sounds[random.randint(0, 4)].play()
                    self.last_move_time = time.time()
                elif right and current_time - self.last_move_time > DELTA_TIME:
                    self.go_logic.regret()
                    self.last_move_time = time.time()

    @staticmethod
    def reset_judgement() -> bool:
        x, y = pygame.mouse.get_pos()

        x_pos = (OPENING_OPTION_WHITE_POS[0] + 1) * UNIT + MID_UNIT
        y_pos = (OPENING_OPTION_WHITE_POS[1] + 1) * UNIT + MID_UNIT

        x_delta = abs(x - x_pos)
        y_delta = abs(y - y_pos)

        distance = math.sqrt(x_delta ** 2 + y_delta ** 2)
        radius_range = 1.0 * OPTION_OUTER_RADIUS
        return distance <= radius_range

    def katago_terminate(self):
        self.process.stdin.write('quit\n')
        self.process.stdin.flush()
        self.process.terminate()

    def ai_play(self, take_black, take_white, take_random):
        while True:
            point_to_reset = self.reset_judgement()
            mouse_clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.katago_terminate()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and point_to_reset:
                        mouse_clicked = True

            if mouse_clicked:
                break

            self.visual.self_play_display(self.go_logic.board_info, self.go_logic.last_move, point_to_reset)

            x_num, y_num = self.get_mouse_pos_num()
            if 0 <= x_num <= 18 and 0 <= y_num <= 18:
                left, _, right = pygame.mouse.get_pressed()
                current_time = time.time()
                if left and current_time - self.last_move_time > DELTA_TIME:
                    if self.go_logic.set_stone(x_num, y_num):
                        # gtp_str = coord_to_gtp([x_num, y_num])
                        # print(f"current gtp string: {gtp_str}")
                        # print(f"current cord: ( {x_num}, {y_num})")
                        # back_cord = gtp_to_coord(gtp_str)
                        # print(f"back cord: ( {back_cord[0]}, {back_cord[1]})")
                        self.stone_sounds[random.randint(0, 4)].play()
                    self.last_move_time = time.time()
                elif right and current_time - self.last_move_time > DELTA_TIME:
                    self.go_logic.regret()
                    self.last_move_time = time.time()

    def idle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.katago_terminate()
                sys.exit()
        self.visual.idle_plot()

    def play(self):
        ready_str = "GTP ready, beginning main protocol loop"
        line = self.process.stdout.readline()
        while not (ready_str in line):
            self.idle()
            line = self.process.stdout.readline()
        while True:
            take_black, take_white, take_random = self.opening()
            self.go_logic.reset()

            self.ai_play(take_black, take_white, take_random)
            self.go_logic.reset()

