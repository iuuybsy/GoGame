from enum import Enum


class OccupyStatus(Enum):
    Free = 1
    Black = 2
    White = 3


class StoneBase:
    def __init__(self):
        self.occupy_status = OccupyStatus.Free


class BlackStone(StoneBase):
    def __init__(self):
        StoneBase.__init__(self)
        self.occupy_status = OccupyStatus.Black


class WhiteStone(StoneBase):
    def __init__(self):
        StoneBase.__init__(self)
        self.occupy_status = OccupyStatus.White
