from src.mino.base_mino import BaseMino
from src.utils.constants import *

class MinoO(BaseMino):
    """ O字テトリスブロッククラス """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = MINO_O_ID
        n = self.id
        self._mino_field = [
            [0, 0, 0, 0, 0],
            [0, 0, n, n, 0],
            [0, 0, n, n, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self._initial_field = [[self._mino_field[y][x] for x in range(5)] for y in range(5)]


    def rotate_right(self):
        """ O字ミノは回転の意味がないのでオーバーライドして処理を無効化 """
        pass

    def rotate_left(self):
        """ O字ミノは回転の意味がないのでオーバーライドして処理を無効化 """
        pass

    def init_mino_rotation(self):
        self.Update()