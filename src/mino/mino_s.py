from src.mino.base_mino import BaseMino
from src.utils.constants import *

class MinoS(BaseMino):
    """ S字テトリスブロッククラス """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.y -= 1
        self.id = MINO_S_ID
        n = self.id
        self._mino_field = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, n, n, 0],
            [0, n, n, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self._initial_field = [[self._mino_field[y][x] for x in range(5)] for y in range(5)]