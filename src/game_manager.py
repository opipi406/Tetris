import subprocess, platform
import random
from enum import Enum, auto

from src.config_manager import config
from src.mino.base_mino import BaseMino
from src.mino.mino_i import MinoI
from src.mino.mino_j import MinoJ
from src.mino.mino_l import MinoL
from src.mino.mino_o import MinoO
from src.mino.mino_s import MinoS
from src.mino.mino_t import MinoT
from src.mino.mino_z import MinoZ
from src.utils.constants import *


class GameMode(Enum):
    """ ゲームモード列挙型 """

    NONE = auto()
    AGENT = auto()
    QUICK_AGENT = auto()
    PLAYER = auto()


class GameManager:
    """ テトリスゲーム管理クラス

    .. csv-table:: メンバ変数一覧
        :header: 変数名, 概要
        :widths: 10, 85

        self.score,  | 獲得したゲームスコア獲得したゲームスコア獲得したゲームスコア
        self.field,  テトリスフィールド定義（二次元配列）
        self.mino,   操作中テトリスブロック（テトリミノ）のインスタンス
    """

    __instance = None

    @staticmethod
    def getInstance(**kwargs):
        """ Singletonクラス用インスタンス生成メソッド """
        if GameManager.__instance is None:
            GameManager(**kwargs)
        return GameManager.__instance

    def __init__(self, **kwargs):
        if GameManager.__instance is not None:
            raise Exception("SingletonClassException")
        else:
            GameManager.__instance = self

        # public
        self.game_mode:GameMode = GameMode.NONE
        self.score = 0          # 獲得スコア値
        self.lines = 0          # 消去ライン数
        self.pieces = 0         # 生成テトリミノ数
        self.field = [[0 for x in range(FIELD_BLOCK_X)] for y in range(FIELD_BLOCK_Y)]     # フィールド定義
        self.mino:BaseMino = None       # 操作中テトリスブロック（テトリミノ）インスタンス

        # private
        self._score_label = kwargs['score_label']
        self._lines_label = kwargs['lines_label']
        self._pieces_label = kwargs['pieces_label']
        self._next_canvas = kwargs['next_canvas']

        self._mino_stack = []   # Nextテトリミノをスタックするリスト
        self._score_ratio = 1   # スコア倍率


    def initialized(self):
        """ 初期化メソッド

        このメソッドはゲームスタート時に呼び出される。
        """

        if platform.system() == 'Darwin': subprocess.call('clear')
        print('*** GAME START!! ***')

        self.score = self.lines = self.pieces = 0
        self._score_label['text'] = TEXT_SCORE.format(self.score)
        self._lines_label['text'] = TEXT_LINES.format(self.lines)
        self._pieces_label['text'] = TEXT_PIECES.format(self.pieces)
        self.field = [[0 for x in range(FIELD_BLOCK_X)] for y in range(FIELD_BLOCK_Y)]

        kwargs = {'field': self.field, 'x': INITIAL_MINO_X, 'y': INITIAL_MINO_Y}
        self._mino_stack = [
            MinoI(**kwargs), MinoJ(**kwargs), MinoL(**kwargs), MinoO(**kwargs),
            MinoS(**kwargs), MinoT(**kwargs), MinoZ(**kwargs)
        ]
        random.shuffle(self._mino_stack)
        self.generate_mino()

    @property
    def is_gameover(self):
        """ ゲームオーバー判定プロパティ

        Returns:
            ゲームオーバーならTrue、そうでなければFalseを返却
        """
        for x in self.field[FIELD_BLOCK_OVER_Y]:
            if x != 0 and x != 9:
                return True
        return False

    def generate_mino(self):
        """ テトリミノの生成 """
        self.mino = self._mino_stack.pop(0)
        self.pieces += 1
        self._pieces_label['text'] = TEXT_PIECES.format(self.pieces)

        # 全種類のテトリミノを一巡したらスタックを補充して再度シャッフルする
        if len(self._mino_stack) == 0:
            kwargs = {'field': self.field, 'x': INITIAL_MINO_X, 'y': INITIAL_MINO_Y}
            self._mino_stack = [
                MinoI(**kwargs), MinoJ(**kwargs), MinoL(**kwargs), MinoO(**kwargs),
                MinoS(**kwargs), MinoT(**kwargs), MinoZ(**kwargs)
            ]
            random.shuffle(self._mino_stack)

        self.mino.Update()
        self._next_canvas.Update(self._mino_stack[0])

    def delete_lines(self):
        """ 横一列全て埋まったラインを消去する """

        cnt = 0
        for y in range(FIELD_BLOCK_Y):
            # y行のブロックが全て埋まっている
            if all([x != 0 for x in self.field[y]]):
                cnt += 1
                # 揃った段より上の段から１段下にシフト
                for _y in reversed(range(0, y)):
                    for _x in range(FIELD_BLOCK_X):
                        self.field[_y + 1][_x] = self.field[_y][_x]

        if cnt > 0:
            self.score += SCORE_RATE[min(3, cnt-1)] * self._score_ratio
            self.lines += cnt
            self._score_label['text'] = TEXT_SCORE.format(self.score)
            self._lines_label['text'] = TEXT_LINES.format(self.lines)

    # ===========================================================
    #   更新処理
    # ===========================================================
    def Update(self):
        """ フィールド状態等の更新 """
        self.mino.Update()      # 操作中テトリミノ情報を更新

    def DEBUG(self, field=None):
        """ デバッグ用フィールド出力 """
        # if platform.system() == 'Darwin': subprocess.call('clear')
        if field is None:
            field = self.field

        for y in range(FIELD_BLOCK_Y):
            l = [str(x) if x != 0 else ' ' for x in field[y]]
            line = '.'.join(l)
            if y == FIELD_BLOCK_OVER_Y:
                print('---------------------------')
            print('{:0>2} |{}|'.format(y, line))