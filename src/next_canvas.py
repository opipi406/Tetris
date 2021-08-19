import tkinter as tk

from src.utils.constants import *
from src.color import Color
from src.config_manager import config
from src.mino.base_mino import BaseMino


class NextCanvas(tk.Canvas):
    """ Nextテトリミノ描画キャンバスクラス """

    def __init__(self, app):

        super().__init__(
            app,
            width=5 * BLOCK_SIZE,
            height=5 * BLOCK_SIZE,
            bg="white")

        if not config.GAME.enable_next:
            return

        # キャンバスを画面上に設置
        self.place(x=FIELD_BLOCK_X * BLOCK_SIZE + 50, y=25)

        # フィールドのマスを生成
        for y in range(5):
            for x in range(5):
                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = y * BLOCK_SIZE
                y2 = (y + 1) * BLOCK_SIZE
                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline='white', width=1,
                    fill=Color.GRAY
                )

    # ===========================================================
    #   更新処理
    # ===========================================================
    def Update(self, next_mino:BaseMino):
        """ フィールドの更新 """

        if not config.GAME.enable_next:
            return

        self.delete('all')

        _mino_field = next_mino.mino_field

        # フィールドのマスを生成
        for y in range(5):
            for x in range(5):
                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = y * BLOCK_SIZE
                y2 = (y + 1) * BLOCK_SIZE

                if _mino_field[y][x] != 0:
                    _color = Color.ID(next_mino.id)
                else:
                    _color = Color.GRAY

                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline='white', width=1, fill=_color)

                if _color != Color.GRAY:
                    n = 2
                    self.create_rectangle(
                        x1 + n, y1 + n, x2 - n, y2 - n,
                        outline='white', width=1)