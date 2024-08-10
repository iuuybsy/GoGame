# from game_board import GameBoard
from core_logic import CoreLogic


# x = GameBoard()

logic = CoreLogic()

moves = [[1, 0], [0, 0], [0, 1], [1, 1]]
logic.test_logic(moves)
