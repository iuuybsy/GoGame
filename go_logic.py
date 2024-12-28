import copy

from stone_enum import OccupyStatus

NUM: int = 19
SEARCH_DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]


class Stack:
    def __init__(self):
        self.items: list[tuple[int, int]] = []

    def push(self, item: tuple[int, int]):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def is_empty(self) -> bool:
        return len(self.items) == 0


class GoLogic:
    def __init__(self):
        self.board_info = [[OccupyStatus.Free for _ in range(NUM)] for _ in range(NUM)]
        self.liberty = [[0 for _ in range(NUM)] for _ in range(NUM)]
        self.is_black_turn: bool = True
        self.last_move = [-1, -1]

        self.board_record: list[list[list[OccupyStatus]]] = []
        self.liberty_record: list[list[list[int]]] = []
        self.move_record: list[list[int]] = []

    def check_liberty(self, x: int, y: int) -> int:
        if not self.valid_cord(x, y):
            raise IndexError("Index out of range in GOLogic.check_liberty method")
        elif not self.occupied_by_stone(x, y):
            raise TypeError("The position is not occupied by stone")

        connected_stones: list[tuple[int, int]] = []
        stack = Stack()
        stack.push((x, y))
        unvisited = [[True for _ in range(NUM)] for __ in range(NUM)]

        while not stack.is_empty():
            current_x, current_y = stack.pop()
            unvisited[current_x][current_y] = False
            connected_stones.append((current_x, current_y))
            for direction in SEARCH_DIRECTION:
                next_x = current_x + direction[0]
                next_y = current_y + direction[1]
                if not self.valid_cord(next_x, next_y):
                    continue
                if self.board_info[next_x][next_y] != self.board_info[x][y]:
                    continue
                if unvisited[next_x][next_y]:
                    stack.push((next_x, next_y))

        free_space_set: set[tuple[int, int]] = set()
        for x, y in connected_stones:
            for direction in SEARCH_DIRECTION:
                next_x = x + direction[0]
                next_y = y + direction[1]
                if not self.valid_cord(next_x, next_y):
                    continue
                if not self.occupied_by_stone(next_x, next_y):
                    free_space_set.add((next_x, next_y))
        liberty = len(free_space_set)
        for x, y in connected_stones:
            self.liberty[x][y] = liberty
        if liberty == 0:
            for x, y in connected_stones:
                self.board_info[x][y] = OccupyStatus.Free
        return liberty

    @staticmethod
    def valid_cord(x: int, y: int) -> bool:
        if x < 0 or x >= NUM or y < 0 or y >= NUM:
            return False
        return True

    def occupied_by_stone(self, x: int, y: int) -> bool:
        if self.board_info[x][y] == OccupyStatus.Black:
            return True
        elif self.board_info[x][y] == OccupyStatus.White:
            return True
        return False

    def set_stone(self, x: int, y: int):
        if self.occupied_by_stone(x, y):
            return

        target_status = OccupyStatus.Black if self.is_black_turn else OccupyStatus.White
        hostile_status = OccupyStatus.White if self.is_black_turn else OccupyStatus.Black

        self.board_info[x][y] = target_status
        for direction in SEARCH_DIRECTION:
            next_x = x + direction[0]
            next_y = y + direction[1]
            if not self.valid_cord(next_x, next_y):
                continue
            if self.board_info[next_x][next_y] == hostile_status:
                _ = self.check_liberty(next_x, next_y)

        local_liberty = self.check_liberty(x, y)
        if local_liberty == 0:
            self.board_info = copy.deepcopy(self.board_record[-1])
            self.liberty = copy.deepcopy(self.liberty_record[-1])
            return
        if len(self.move_record) >= 2 and self.board_info == self.board_record[-2]:
            self.board_info = copy.deepcopy(self.board_record[-1])
            self.liberty = copy.deepcopy(self.liberty_record[-1])
            return
        self.is_black_turn = not self.is_black_turn
        self.last_move = [x, y]
        self.board_record.append(copy.deepcopy(self.board_info))
        self.liberty_record.append(copy.deepcopy(self.liberty))
        self.move_record.append([x, y])

    def regret(self):
        if len(self.move_record) == 0:
            return
        self.board_record.pop()
        self.liberty_record.pop()
        self.move_record.pop()

        if len(self.move_record) == 0:
            self.board_info = [[OccupyStatus.Free for _ in range(NUM)] for _ in range(NUM)]
            self.liberty = [[0 for _ in range(NUM)] for _ in range(NUM)]
            self.is_black_turn = True
            self.last_move = [-1, -1]
            return

        self.board_info = copy.deepcopy(self.board_record[-1])
        self.liberty = copy.deepcopy(self.liberty_record[-1])
        self.last_move = self.move_record[-1]
        self.is_black_turn = not self.is_black_turn
