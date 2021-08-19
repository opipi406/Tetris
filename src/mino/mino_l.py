from src.mino.base_mino import BaseMino
from src.utils.constants import *

class MinoL(BaseMino):
    """ L字テトリスブロッククラス """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = MINO_L_ID
        n = self.id
        self._mino_field = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, n, 0],
            [0, n, n, n, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self._initial_field = [[self._mino_field[y][x] for x in range(5)] for y in range(5)]

    def init_mino_rotation(self):
        self.Update()