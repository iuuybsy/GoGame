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
        self.liberty_info: list[list[int]] = [[4 for _ in range(19)] for __ in range(19)]
        self.count: int = 0
        self.finish: bool = False
        self.last_move_is_passed: bool = False
        self.black_turn: bool = True

    def check_liberty(self, x: int, y: int):
        if self.board_info[x][y] == OccupyStatus.Free:
            self.liberty_info[x][y] = 0
            return
        stone_type = self.board_info[x][y]
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
                if self.board_info[x_temp][y_temp] == stone_type:
                    if liberty_count[x_temp][y_temp]:
                        stack.push((x_temp, y_temp))
                        liberty_count[x_temp][y_temp] = False
                if self.board_info[x_temp][y_temp] == OccupyStatus.Free:
                    if liberty_count[x_temp][y_temp]:
                        local_liberty += 1
                        liberty_count[x_temp][y_temp] = False
        liberty_count.clear()
        liberty_count = [[True for _ in range(19)] for __ in range(19)]
        liberty_count[x][y] = False
        stack.push((x, y))
        if local_liberty == 0:
            while not stack.empty():
                x_cri, y_cri = stack.top()
                stack.pop()
                self.board_info[x_cri][y_cri] = OccupyStatus.Free
                self.liberty_info[x_cri][y_cri] = 0
                for i in range(4):
                    x_temp = x_cri + DIRECTIONS[i][0]
                    y_temp = y_cri + DIRECTIONS[i][1]
                    if x_temp < 0 or x_temp >= 19 or y_temp < 0 or y_temp >= 19:
                        continue
                    if self.board_info[x_temp][y_temp] == stone_type:
                        if liberty_count[x_temp][y_temp]:
                            stack.push((x_temp, y_temp))
                            liberty_count[x_temp][y_temp] = False
        else:
            while not stack.empty():
                x_cri, y_cri = stack.top()
                stack.pop()
                self.liberty_info[x_cri][y_cri] = local_liberty
                for i in range(4):
                    x_temp = x_cri + DIRECTIONS[i][0]
                    y_temp = y_cri + DIRECTIONS[i][1]
                    if x_temp < 0 or x_temp >= 19 or y_temp < 0 or y_temp >= 19:
                        continue
                    if self.board_info[x_temp][y_temp] == stone_type:
                        if liberty_count[x_temp][y_temp]:
                            stack.push((x_temp, y_temp))
                            liberty_count[x_temp][y_temp] = False

    def set_black_stone(self, x: int, y: int):
        if self.board_info[x][y] == OccupyStatus.Free:
            self.board_info[x][y] = OccupyStatus.Black
            self.check_liberty(x, y)
            self.black_turn = False;

    def set_white_stone(self, x: int, y: int):
        if self.board_info[x][y] == OccupyStatus.Free:
            self.board_info[x][y] = OccupyStatus.White
            self.check_liberty(x, y)
            self.black_turn = True

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

    def board_render(self):
        fig, ax = plt.subplots(figsize=(8, 8))
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

        ax.set_aspect(1)
        plt.xlim((-0.5, 18.5))
        plt.ylim((-0.5, 18.5))
        plt.axis('off')
        plt.show()

