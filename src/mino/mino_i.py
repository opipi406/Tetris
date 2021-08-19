from src.mino.base_mino import BaseMino, KeyEvent
from src.utils.constants import *


class MinoI(BaseMino):
    """ I字テトリスブロッククラス """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = MINO_I_ID
        n = self.id
        self._mino_field = [
            [0, 0, 0, 0, 0],
            [0, n, n, n, n],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self._initial_field = [[self._mino_field[y][x] for x in range(5)] for y in range(5)]
        self._rota_state = 0
        self._prev_rota_state = 0

    def rotate_right(self):
        self.backup_position()
        self._rotate_adjust_cnt = 0

        self._rota_state += 1
        if self._rota_state == 4:
            self._rota_state = 0

        self._mino_field = self._rotate()
        self.prev_key_event = KeyEvent.ROTATE_RIGHT

    def rotate_left(self):
        self.backup_position()
        self._rotate_adjust_cnt = 0

        self._rota_state -= 1
        if self._rota_state == -1:
            self._rota_state = 3

        self._mino_field = self._rotate()
        self.prev_key_event = KeyEvent.ROTATE_LEFT

    def _rotate(self):
        """ I字テトリミノのみ角度によって回転軸が変化するため、力技で実装 """
        n = self.id
        if self._rota_state == 0:
            return [
                [0, 0, 0, 0, 0],
                [0, n, n, n, n],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        elif self._rota_state == 1:
            return [
                [0, 0, 0, n, 0],
                [0, 0, 0, n, 0],
                [0, 0, 0, n, 0],
                [0, 0, 0, n, 0],
                [0, 0, 0, 0, 0],
            ]
        elif self._rota_state == 2:
            return [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, n, n, n, n],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        elif self._rota_state == 3:
            return [
                [0, 0, n, 0, 0],
                [0, 0, n, 0, 0],
                [0, 0, n, 0, 0],
                [0, 0, n, 0, 0],
                [0, 0, 0, 0, 0],
            ]

    def backup_position(self):
        super().backup_position()
        self._prev_rota_state = self._rota_state

    def rollback_position(self):
        super().rollback_position()
        self._rota_state = self._prev_rota_state