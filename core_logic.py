import copy
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from stones import OccupyStatus

DIRECTIONS = [[1, 0], [0, 1], [-1, 0], [0, -1]]


class Stack:
    def __init__(self):
        self.stack = []

    def empty(self):
        return len(self.stack) == 0

    def top(self):
        if not self.empty():
            return self.stack[-1]

    def pop(self):
        if not self.empty():
            self.stack.pop()

    def push(self, element):
        self.stack.append(element)


class CoreLogic:
    def __init__(self):
        self.board_info = [[OccupyStatus.Free for _ in range(19)] for __ in range(19)]
        self.liberty_info: list[list[int]] = [[0 for _ in range(19)] for __ in range(19)]
        self.black_turn: bool = True
        self.valid: bool = True
        self.situation = []
        self.ko = [-1, -1]
        self.last_move = [-1, -1]

    def test_logic(self, moves: list):
        for i in range(len(moves)):
            x, y = moves[i]
            self.set_stone(x, y)
            self.board_render(x, y)

    def clear_board(self):
        self.board_info.clear()
        self.board_info = [[OccupyStatus.Free for _ in range(19)] for __ in range(19)]
        self.liberty_info.clear()
        self.liberty_info: list[list[int]] = [[0 for _ in range(19)] for __ in range(19)]
        self.black_turn: bool = True
        self.valid: bool = True
        self.situation.clear()
        self.ko = [-1, -1]
        self.last_move = [-1, -1]

    def check_liberty(self, x: int, y: int):
        self.check_hostile_liberty(x, y)
        self.check_friendly_liberty(x, y)

    def is_occupied_by_stone(self, x: int, y: int) -> bool:
        test1 = self.board_info[x][y] == OccupyStatus.White
        test2 = self.board_info[x][y] == OccupyStatus.Black
        return test1 or test2

    def is_connected(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        if x1 == x2 and y1 == y2:
            return True
        if not self.is_occupied_by_stone(x1, y1):
            return False
        if not self.is_occupied_by_stone(x2, y2):
            return False
        if self.board_info[x1][y1] != self.board_info[x2][y2]:
            return False
        stack = Stack()
        stack.push((x1, y1))
        liberty_count: list[list[bool]] = [[True for _ in range(19)] for __ in range(19)]
        liberty_count[x1][y1] = False
        local_status = self.board_info[x1][y1]
        while not stack.empty():
            x_cri, y_cri = stack.top()
            stack.pop()
            for i in range(4):
                x_temp = x_cri + DIRECTIONS[i][0]
                y_temp = y_cri + DIRECTIONS[i][1]
                if x_temp < 0 or x_temp >= 19 or y_temp < 0 or y_temp >= 19:
                    continue
                if self.board_info[x_temp][y_temp] == local_status:
                    if x_temp == x2 and y_temp == y2:
                        return True
                    if liberty_count[x_temp][y_temp]:
                        stack.push((x_temp, y_temp))
                        liberty_count[x_temp][y_temp] = False
        return False

    def get_local_liberty(self, x: int, y: int) -> int:
        if not self.is_occupied_by_stone(x, y):
            return 0
        local_status = self.board_info[x][y]
        stack = Stack()
        stack.push((x, y))
        local_liberty: int = 0
        liberty_count: list[list[bool]] = [[True for _ in range(19)] for __ in range(19)]
        liberty_count[x][y] = False
        while not stack.empty():
            x_cri, y_cri = stack.top()
            stack.pop()
            for i in range(4):
                x_temp = x_cri + DIRECTIONS[i][0]
                y_temp = y_cri + DIRECTIONS[i][1]
                if x_temp < 0 or x_temp >= 19 or y_temp < 0 or y_temp >= 19:
                    continue
                if self.board_info[x_temp][y_temp] == local_status:
                    if liberty_count[x_temp][y_temp]:
                        stack.push((x_temp, y_temp))
                        liberty_count[x_temp][y_temp] = False
                if self.board_info[x_temp][y_temp] == OccupyStatus.Free:
                    if liberty_count[x_temp][y_temp]:
                        local_liberty += 1
                        liberty_count[x_temp][y_temp] = False
        return local_liberty

    def set_local_liberty(self, x: int, y: int, local_liberty: int):
        if not self.is_occupied_by_stone(x, y):
            return
        local_status = self.board_info[x][y]
        stack = Stack()
        stack.push((x, y))
        liberty_count: list[list[bool]] = [[True for _ in range(19)] for __ in range(19)]
        liberty_count[x][y] = False
        count: int = 0
        while not stack.empty():
            x_cri, y_cri = stack.top()
            stack.pop()
            self.liberty_info[x_cri][y_cri] = local_liberty
            if local_liberty == 0:
                self.board_info[x_cri][y_cri] = OccupyStatus.Free
                count += 1
            for i in range(4):
                x_temp = x_cri + DIRECTIONS[i][0]
                y_temp = y_cri + DIRECTIONS[i][1]
                if x_temp < 0 or x_temp >= 19 or y_temp < 0 or y_temp >= 19:
                    continue
                if self.board_info[x_temp][y_temp] == local_status:
                    if liberty_count[x_temp][y_temp]:
                        stack.push((x_temp, y_temp))
                        liberty_count[x_temp][y_temp] = False
        if count == 1:
            self.ko[0], self.ko[1] = x, y

    def check_hostile_liberty(self, x: int, y: int):
        hostile_status = OccupyStatus.White
        if self.board_info[x][y] == OccupyStatus.White:
            hostile_status = OccupyStatus.Black
        hostile_list = []
        for i in range(4):
            x_temp = x + DIRECTIONS[i][0]
            y_temp = y + DIRECTIONS[i][1]
            if x_temp < 0 or x_temp >= 19 or y_temp < 0 or y_temp >= 19:
                continue
            if self.board_info[x_temp][y_temp] == hostile_status:
                if len(hostile_list) == 0:
                    hostile_list.append((x_temp, y_temp))
                else:
                    for j in range(len(hostile_list)):
                        x_hos, y_hos = hostile_list[j]
                        if not self.is_connected(x_temp, y_temp, x_hos, y_hos):
                            hostile_list.append((x_temp, y_temp))
        for i in range(len(hostile_list)):
            x_hos, y_hos = hostile_list[i]
            local_liberty = self.get_local_liberty(x_hos, y_hos)
            self.set_local_liberty(x_hos, y_hos, local_liberty)

    def check_friendly_liberty(self, x: int, y: int):
        local_liberty = self.get_local_liberty(x, y)
        self.set_local_liberty(x, y, local_liberty)

    def check_valid(self, x: int, y: int):
        if self.black_turn:
            self.board_info[x][y] = OccupyStatus.Black
        else:
            self.board_info[x][y] = OccupyStatus.White
        local_liberty = self.get_local_liberty(x, y)
        if local_liberty > 0:
            self.board_info[x][y] = OccupyStatus.Free
            return True

        hostile_status = OccupyStatus.White
        if self.board_info[x][y] == OccupyStatus.White:
            hostile_status = OccupyStatus.Black
        hostile_list = []
        for i in range(4):
            x_temp = x + DIRECTIONS[i][0]
            y_temp = y + DIRECTIONS[i][1]
            if x_temp < 0 or x_temp >= 19 or y_temp < 0 or y_temp >= 19:
                continue
            if self.board_info[x_temp][y_temp] == hostile_status:
                if len(hostile_list) == 0:
                    hostile_list.append((x_temp, y_temp))
                else:
                    for j in range(len(hostile_list)):
                        x_hos, y_hos = hostile_list[j]
                        if not self.is_connected(x_temp, y_temp, x_hos, y_hos):
                            hostile_list.append((x_temp, y_temp))
        for i in range(len(hostile_list)):
            x_hos, y_hos = hostile_list[i]
            local_liberty = self.get_local_liberty(x_hos, y_hos)
            if local_liberty == 0:
                self.board_info[x][y] = OccupyStatus.Free
                return True
        self.board_info[x][y] = OccupyStatus.Free
        return False

    def set_black_stone(self, x: int, y: int):
        if self.board_info[x][y] == OccupyStatus.Free:
            self.board_info[x][y] = OccupyStatus.Black
            self.black_turn = False
            self.check_liberty(x, y)

    def set_white_stone(self, x: int, y: int):
        if self.board_info[x][y] == OccupyStatus.Free:
            self.board_info[x][y] = OccupyStatus.White
            self.black_turn = True
            self.check_liberty(x, y)

    def set_stone(self, x: int, y: int):
        self.valid = self.check_valid(x, y)
        if self.valid:
            if x != self.ko[0] or y != self.ko[1]:
                self.valid = True
                self.ko[0], self.ko[1] = -1, -1
                if self.black_turn:
                    self.set_black_stone(x, y)
                else:
                    self.set_white_stone(x, y)
                board_info = copy.deepcopy(self.board_info)
                liberty_info = copy.deepcopy(self.liberty_info)
                self.situation.append((board_info, liberty_info))

    def pass_this_move(self):
        self.black_turn = not self.black_turn

    def regret(self):
        if len(self.situation) > 1:
            self.board_info.clear()
            self.liberty_info.clear()
            self.situation.pop()
            self.board_info, self.liberty_info = self.situation[-1]
            self.black_turn = not self.black_turn

        elif len(self.situation) == 1:
            self.clear_board()

    @classmethod
    def board_render(cls, board_info, x=19, y=19):
        fig, ax = plt.subplots(figsize=(6, 6))
        plt.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)

        for i in range(19):
            ax.plot([0, 18], [i, i], c='black')
            ax.plot([i, i], [0, 18], c='black')

        star_points = [[3, 3], [15, 3], [3, 15], [15, 15],
                       [3, 9], [9, 3], [9, 15], [15, 9], [9, 9]]
        for i in range(len(star_points)):
            ax.scatter(star_points[i][0], star_points[i][1], marker='o', c='black')

        for i in range(19):
            for j in range(19):
                if board_info[i][j] == OccupyStatus.Free:
                    continue
                elif board_info[i][j] == OccupyStatus.Black:
                    c = Circle(xy=(i, 18 - j), radius=0.45, color='black', zorder=2)
                    plt.gca().add_patch(c)
                elif board_info[i][j] == OccupyStatus.White:
                    c1 = Circle(xy=(i, 18 - j), radius=0.45, color='black', zorder=2)
                    plt.gca().add_patch(c1)
                    c2 = Circle(xy=(i, 18 - j), radius=0.35, color='white', zorder=2)
                    plt.gca().add_patch(c2)
        if x < 19 and y < 19:
            if board_info[x][y] == OccupyStatus.White:
                c = Circle(xy=(x, 18 - y), radius=0.2, color='red', zorder=3)
                plt.gca().add_patch(c)
            if board_info[x][y] == OccupyStatus.Black:
                c = Circle(xy=(x, 18 - y), radius=0.2, color='red', zorder=3)
                plt.gca().add_patch(c)

        ax.set_aspect(1)
        plt.xlim((-0.5, 18.5))
        plt.ylim((-0.5, 18.5))
        plt.axis('off')
        plt.show()

