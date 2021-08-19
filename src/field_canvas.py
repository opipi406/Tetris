import tkinter as tk

from src.utils.constants import *
from src.color import Color
from src.game_manager import GameManager, GameMode


class FieldCanvas(tk.Canvas):
    """ フィールド描画キャンバスクラス """

    def __init__(self, app, _gameMgr:GameManager):

        super().__init__(
            app,
            width=FIELD_BLOCK_X * BLOCK_SIZE,
            height=(FIELD_BLOCK_Y - FIELD_BLOCK_OVER_Y) * BLOCK_SIZE,
            bg="white")

        self._gameMgr = _gameMgr

        # キャンバスを画面上に設置
        self.place(x=25, y=25)

        # フィールドのマスを生成
        for y in range(FIELD_BLOCK_OVER_Y, FIELD_BLOCK_Y):
            for x in range(FIELD_BLOCK_X):
                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = (y - FIELD_BLOCK_OVER_Y) * BLOCK_SIZE
                y2 = (y + 1 - FIELD_BLOCK_OVER_Y) * BLOCK_SIZE
                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline='white', width=1,
                    fill=Color.GRAY
                )

    # ===========================================================
    #   更新処理
    # ===========================================================
    def Update(self):
        """ フィールドの更新 """
        if self._gameMgr.game_mode == GameMode.QUICK_AGENT and not self._gameMgr.is_gameover:
            return

        self.delete('all')
        # フィールドのマスを生成
        for y in range(FIELD_BLOCK_OVER_Y, FIELD_BLOCK_Y):
            for x in range(FIELD_BLOCK_X):
                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = (y - FIELD_BLOCK_OVER_Y) * BLOCK_SIZE
                y2 = (y + 1 - FIELD_BLOCK_OVER_Y) * BLOCK_SIZE

                if self._gameMgr.field[y][x] == 9:
                    _color = Color.ID(self._gameMgr.mino.id)
                else:
                    _color = Color.ID(self._gameMgr.field[y][x])

                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline='white', width=1, fill=_color)

                if _color != Color.GRAY:
                    n = 2
                    self.create_rectangle(
                        x1 + n, y1 + n, x2 - n, y2 - n,
                        outline='white', width=1)
