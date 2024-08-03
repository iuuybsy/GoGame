# from game_board import GameBoard
from core_logic import CoreLogic


# x = GameBoard()

logic = CoreLogic()
for i in range(19):
    for j in range(19):
        logic.set_stone(i, j)
logic.board_render()
