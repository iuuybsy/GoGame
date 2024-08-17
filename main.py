from game_board import GameBoard
# from core_logic import CoreLogic
import sgf_file_load


x = GameBoard()

# logic = CoreLogic()

adv_black, adv_white, moves, black_first = sgf_file_load.load_sgf_file("test_sgf4.sgf")
# logic.test_logic(moves)
x.logic_test(adv_black, adv_white, moves, black_first)

# x.self_play()
