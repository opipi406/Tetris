import tkinter as tk
import itertools

from src.utils.constants import *
from src.config_manager import config
from src.game_manager import GameManager, GameMode
from src.field_canvas import FieldCanvas
from src.next_canvas import NextCanvas


class Application(tk.Tk):
    """ アプケーションクラス """

    def __init__(self):
        super().__init__()

        self.episodes = 0       # 試行回数（エピソード数）

        # アプリウィンドウの設定
        self.geometry('%dx%d' % (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.title("テトリス")

        # ===========================================================
        #   ウィジェットの配置
        # ===========================================================
        btn_positions = (
            {'x': 25,   'y': WINDOW_HEIGHT - 50},
            {'x': 200,  'y': WINDOW_HEIGHT - 50},
        )
        # 開始ボタン
        tk.Button(self, text='Start', width=15, command=self.onClickStart)\
            .place(**btn_positions[0])
        # 停止ボタン
        tk.Button(self, text='Stop', width=15, command=self.onClickStop)\
            .place(**btn_positions[1])

        offset_y = itertools.count(start=200, step=30)
        # 獲得スコア
        score_label = tk.Label(self, text=TEXT_SCORE.format(0), font=FONT)
        score_label.place(x=FIELD_BLOCK_X * BLOCK_SIZE + 50, y=next(offset_y))
        # 消去ライン数
        lines_label = tk.Label(self, text=TEXT_LINES.format(0), font=FONT)
        lines_label.place(x=FIELD_BLOCK_X * BLOCK_SIZE + 50, y=next(offset_y))
        # 生成テトリミノ数
        pieces_label = tk.Label(self, text=TEXT_PIECES.format(0), font=FONT)
        pieces_label.place(x=FIELD_BLOCK_X * BLOCK_SIZE + 50, y=next(offset_y))
        next(offset_y)

        # Nextテトリミノキャンバス
        self.next_canvas = NextCanvas(self)
        # ゲーム管理インスタンス
        self.gameMgr:GameManager = GameManager.getInstance(
            score_label=score_label,
            lines_label=lines_label,
            pieces_label=pieces_label,
            next_canvas=self.next_canvas,
        )
        # テトリスフィールドキャンバス
        self.field_canvas = FieldCanvas(self, self.gameMgr)

        self.running = False        # ゲーム稼働フラグ
        self.update_event = None    # ループタイマーイベントを格納する変数


    # ===========================================================
    #   更新処理
    # ===========================================================
    def Update(self):
        if not self.running: return

        self.onPressDown(None)
        self.update_event = self.after(config.GAME.refresh_ms, self.Update)


    # ===========================================================
    #   ボタンクリックイベント
    # ===========================================================
    def onClickStart(self):
        if self.running: return

        # イベントハンドラのバインド
        self.bind('<Right>', self.onPressRight)
        self.bind('<Left>', self.onPressLeft)
        self.bind('<Up>', self.onPressUp)
        self.bind('<Down>', self.onPressDown)
        self.bind('<x>', self.onPressX)
        self.bind('<z>', self.onPressZ)

        self.running = True
        self.gameMgr.game_mode = GameMode.PLAYER
        self.gameMgr.initialized()
        self.field_canvas.Update()

        self.update_event = self.after(config.GAME.refresh_ms, self.Update)

    # ===========================================================
    #   キー入力イベント
    # ===========================================================
    def onPressUp(self, e):
        """ 上矢印キー入力イベント """
        self.gameMgr.mino.hard_drop()
        self.gameMgr.Update()

        # テトリミノ固定フラグが立っている
        if self.gameMgr.mino.is_fixed:
            self.gameMgr.mino.fix()     # 操作中テトリミノをフィールドに固定
            self.gameMgr.delete_lines() # 揃ったラインの消去

            if self.gameMgr.is_gameover:
                print('*** GAME OVER ***')
                self.onClickStop()
                return
            else:
                self.gameMgr.generate_mino()    # 新たなテトリミノを生成

        self.field_canvas.Update()

    def onPressRight(self, e):
        """ 右矢印キー入力イベント """
        self.gameMgr.mino.move_right()
        self.gameMgr.Update()
        self.field_canvas.Update()

    def onPressLeft(self, e):
        """ 左矢印キー入力イベント """
        self.gameMgr.mino.move_left()
        self.gameMgr.Update()
        self.field_canvas.Update()

    def onPressDown(self, e):
        """ 下矢印キー入力イベント """
        self.gameMgr.mino.fall()
        self.gameMgr.Update()

        # テトリミノ固定フラグが立っている
        if self.gameMgr.mino.is_fixed:
            self.gameMgr.mino.fix()     # 操作中テトリミノをフィールドに固定
            self.gameMgr.delete_lines() # 揃ったラインの消去

            if self.gameMgr.is_gameover:
                print('*** GAME OVER ***')
                self.onClickStop()
                return
            else:
                self.gameMgr.generate_mino()    # 新たなテトリミノを生成

        self.field_canvas.Update()

    def onPressX(self, e):
        """ Xキー入力イベント """
        self.gameMgr.mino.rotate_right()
        self.gameMgr.Update()
        self.field_canvas.Update()

    def onPressZ(self, e):
        """ Zキー入力イベント """
        self.gameMgr.mino.rotate_left()
        self.gameMgr.Update()
        self.field_canvas.Update()


    def onClickStop(self):
        """ ゲーム中断ボタン入力イベント """
        if self.running:
            self.running = False

            if self.update_event is not None:
                self.after_cancel(self.update_event)

            # ブロックを灰色にする
            for x in range(FIELD_BLOCK_X):
                for y in range(FIELD_BLOCK_Y):
                    if self.gameMgr.field[y][x] != 0:
                        self.gameMgr.field[y][x] = -1

            self.field_canvas.Update()

            # イベントハンドラのバインドを解除
            self.unbind("<Right>")
            self.unbind("<Left>")
            self.unbind("<Up>")
            self.unbind("<Down>")
            self.unbind("<x>")
            self.unbind("<z>")


if __name__ == "__main__":
    config.initialized()

    app = Application()
    app.mainloop()