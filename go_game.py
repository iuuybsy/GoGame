import pygame
import sys
import time

from visual import Visual
from go_logic import GoLogic

UNIT: int = 41
DELTA_TIME = 0.5


class GoGame:
    def __init__(self):
        pygame.init()
        self.go_logic = GoLogic()
        self.visual = Visual()
        self.last_move_time = time.time()

    def play(self):
        while True:
            self.visual.display(self.go_logic.board_info, self.go_logic.last_move)
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
