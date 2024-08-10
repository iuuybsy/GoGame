from game_board import GameBoard
# from core_logic import CoreLogic
import sgf_file_load


x = GameBoard()

# logic = CoreLogic()

moves = sgf_file_load.load_sgf_file("test_sgf1.sgf")
# logic.test_logic(moves)
x.logic_test(moves)

