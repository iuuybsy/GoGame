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
        self.count: int = 0
        self.finish: bool = False
        self.last_move_is_passed: bool = False
        self.black_turn: bool = True
        self.take_happened: bool = False

    def test_logic(self, moves: list):
        for i in range(len(moves)):
            x, y = moves[i]
            self.set_stone(x, y)
            self.board_render(x, y)

    def check_liberty(self, x: int, y: int):
        self.check_hostile_liberty(x, y)
        self.check_friendly_liberty(x, y)
        # if self.take_happened:
        #     self.take_happened = False
        #     self.check_hostile_liberty(x, y)
        # for j in range(19):
        #     for i in range(19):
        #         print(self.liberty_info[i][j], end="  ")
        #     print("  ")
        # print("  ")

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
        while not stack.empty():
            x_cri, y_cri = stack.top()
            stack.pop()
            self.liberty_info[x_cri][y_cri] = local_liberty
            if local_liberty == 0:
                self.board_info[x_cri][y_cri] = OccupyStatus.Free
            for i in range(4):
                x_temp = x_cri + DIRECTIONS[i][0]
                y_temp = y_cri + DIRECTIONS[i][1]
                if x_temp < 0 or x_temp >= 19 or y_temp < 0 or y_temp >= 19:
                    continue
                if self.board_info[x_temp][y_temp] == local_status:
                    if liberty_count[x_temp][y_temp]:
                        stack.push((x_temp, y_temp))
                        liberty_count[x_temp][y_temp] = False

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
                    flag: bool = True
                    for j in range(len(hostile_list)):
                        x_hos, y_hos = hostile_list[j]
                        if self.is_connected(x_temp, y_temp, x_hos, y_hos):
                            flag = False
                            break
                        if flag:
                            hostile_list.append((x_temp, y_temp))
        for i in range(len(hostile_list)):
            x_hos, y_hos = hostile_list[i]
            local_liberty = self.get_local_liberty(x_hos, y_hos)
            self.set_local_liberty(x_hos, y_hos, local_liberty)

    def check_friendly_liberty(self, x: int, y: int):
        local_liberty = self.get_local_liberty(x, y)
        self.set_local_liberty(x, y, local_liberty)

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
        if self.black_turn:
            self.set_black_stone(x, y)
        else:
            self.set_white_stone(x, y)

    def pass_this_move(self):
        if self.last_move_is_passed:
            self.finish = True
            return
        self.last_move_is_passed = True
        self.black_turn = not self.black_turn

    def board_render(self, x=19, y=19):
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
                if self.board_info[i][j] == OccupyStatus.Free:
                    continue
                elif self.board_info[i][j] == OccupyStatus.Black:
                    c = Circle(xy=(i, 18 - j), radius=0.45, color='black', zorder=2)
                    plt.gca().add_patch(c)
                elif self.board_info[i][j] == OccupyStatus.White:
                    c1 = Circle(xy=(i, 18 - j), radius=0.45, color='black', zorder=2)
                    plt.gca().add_patch(c1)
                    c2 = Circle(xy=(i, 18 - j), radius=0.35, color='white', zorder=2)
                    plt.gca().add_patch(c2)
        if x < 19 and y < 19:
            if self.board_info[x][y] == OccupyStatus.White:
                c = Circle(xy=(x, 18 - y), radius=0.2, color='red', zorder=3)
                plt.gca().add_patch(c)
            if self.board_info[x][y] == OccupyStatus.Black:
                c = Circle(xy=(x, 18 - y), radius=0.2, color='red', zorder=3)
                plt.gca().add_patch(c)

        ax.set_aspect(1)
        plt.xlim((-0.5, 18.5))
        plt.ylim((-0.5, 18.5))
        plt.axis('off')
        plt.show()

