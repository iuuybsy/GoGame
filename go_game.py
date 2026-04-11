import pygame
import sys
import time

from enum import Enum
from visual import Visual
from go_logic import GoLogic
from common.const import UNIT, DELTA_TIME

from sgf_process import sgf_read

class LogicFlow(Enum):
    MoveToOpening = 1,
    MoveToSelfPlay = 2,
    MoveToAiPlay = 3,
    MoveToEnd = 4


class GoGame:
    def __init__(self):
        pygame.init()
        self.go_logic = GoLogic()
        self.visual = Visual()
        self.last_move_time = time.time()

    def opening(self):
        moves = sgf_read("opening.sgf")
        last_move_time = time.time()
        ind = 0
        while ind < len(moves):
            self.visual.opening_display(self.go_logic.board_info, self.go_logic.last_move)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            x_num, y_num = moves[ind]
            self.go_logic.set_stone(x_num, y_num)
            if time.time() - last_move_time > 1:
                ind += 1
                last_move_time = time.time()
        while True:
            self.visual.opening_display(self.go_logic.board_info, [-1, -1])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

    def self_play(self) -> LogicFlow:
        while True:
            self.visual.self_play_display(self.go_logic.board_info, self.go_logic.last_move)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            x, y = pygame.mouse.get_pos()
            x_num = x // UNIT - 1
            y_num = y // UNIT - 1
            if 0 <= x_num <= 18 and 0 <= y_num <= 18:
                left, _, right = pygame.mouse.get_pressed()
                current_time = time.time()
                if left and current_time - self.last_move_time > DELTA_TIME:
                    self.go_logic.set_stone(x_num, y_num)
                    self.last_move_time = time.time()
                elif right and current_time - self.last_move_time > DELTA_TIME:
                    self.go_logic.regret()
                    self.last_move_time = time.time()
        return LogicFlow.MoveToOpening

    def ai_play(self) -> LogicFlow:
        pass

    def end(self):
        pass

    def play(self):
        while True:
            self.visual.self_play_display(self.go_logic.board_info, self.go_logic.last_move)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            x, y = pygame.mouse.get_pos()
            x_num = x // UNIT - 1
            y_num = y // UNIT - 1
            if 0 <= x_num <= 18 and 0 <= y_num <= 18:
                left, _, right = pygame.mouse.get_pressed()
                current_time = time.time()
                if left and current_time - self.last_move_time > DELTA_TIME:
                    self.go_logic.set_stone(x_num, y_num)
                    self.last_move_time = time.time()
                elif right and current_time - self.last_move_time > DELTA_TIME:
                    self.go_logic.regret()
                    self.last_move_time = time.time()
