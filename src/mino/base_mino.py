from abc import ABCMeta
from enum import Enum, auto
import copy

from src.utils.constants import *


class KeyEvent(Enum):
    """ キーイベント列挙型 """

    MOVE_RIGHT = auto()
    MOVE_LEFT = auto()
    ROTATE_RIGHT = auto()
    ROTATE_LEFT = auto()
    FALL = auto()
    IDLE = auto()


class BaseMino(metaclass=ABCMeta):
    """ テトリミノ（テトリスブロック）抽象クラス

    全てのテトリミノクラスはこのクラスを継承する。

    .. csv-table:: メンバ変数一覧
        :header: 変数名, 概要
        :widths: 10, 85

        self.x,                 テトリミノフィールドの中心X座標
        self.y,                 テトリミノフィールドの中心Y座標
        self.id,                テトリミノ識別ID
        self.is_fixed,          テトリミノ固定フラグ
        self.prev_key_event,    直前に入力していたキーイベント
    """

    def __init__(self, **kwargs):
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.id = -1
        self.is_fixed = False
        self.prev_key_event: KeyEvent = KeyEvent.IDLE


        self._field = kwargs['field']   # フィールド情報の参照
        self._mino_field = [[0, 0, 0, 0, 0] for _ in range(5)]  # 5x5のテトリミノフィールド情報
        self._initial_field = []

        # 座標・フィールド情報保持変数
        self._prev_x = 0
        self._prev_y = 0
        self._prev_mino_field = [[0, 0, 0, 0, 0] for _ in range(5)]

        self._rotate_adjust_cnt = 0     # 回転壁蹴り補正回数
        self._fix_duration_cnt = 5      # テトリミノ固定の猶予時間が保証される回数

        # 壁蹴り補正パターン（x, y）
        self._adjust_pattern = (
            (1, 0), (-1, 0),
            (0, 1), (1, 1), (-1, 1),
            (0, 2), (1, 2), (-1, 2),
            (0, -1), (1, -1), (-1, -1),
            (2, 0), (-2, 0),
        )


    def DEBUG(self, field=None):
        """ デバッグ用フィールド出力 """
        # if platform.system() == 'Darwin': subprocess.call('clear')
        if field is None:
            field = self._field

        for y in range(FIELD_BLOCK_Y):
            l = [str(x) if x != 0 else ' ' for x in field[y]]
            line = '.'.join(l)
            if y == FIELD_BLOCK_OVER_Y:
                print('---------------------------')
            print('{:0>2} |{}|'.format(y, line))

    def Update(self):
        """ 更新処理 """

        for x in range(FIELD_BLOCK_X):
            for y in range(FIELD_BLOCK_Y):
                if self._field[y][x] == 9:
                    self._field[y][x] = 0

        for i, x in zip(range(5), range(self.x - 2, self.x + 3)):
            for j, y in zip(range(5), range(self.y - 2, self.y + 3)):

                if self._mino_field[j][i] != 0:

                    # テトリミノの衝突補正
                    #   ブロックが衝突する場合は直前の座標に戻し、衝突が発生しなくなるまで再起的にself.Update()を呼び出す
                    if not ((0 <= x < FIELD_BLOCK_X) and (0 <= y < FIELD_BLOCK_Y) and self._field[y][x] == 0):
                        # 右移動
                        if self.prev_key_event is KeyEvent.MOVE_RIGHT:
                            self.x -= 1
                            self.prev_key_event = KeyEvent.MOVE_RIGHT
                        # 左移動
                        elif self.prev_key_event is KeyEvent.MOVE_LEFT:
                            self.x += 1
                            self.prev_key_event = KeyEvent.MOVE_LEFT
                        # 右回転
                        elif self.prev_key_event is KeyEvent.ROTATE_RIGHT:
                            self.rotate_adjust(KeyEvent.ROTATE_RIGHT)
                        # 左回転
                        elif self.prev_key_event is KeyEvent.ROTATE_LEFT:
                            self.rotate_adjust(KeyEvent.ROTATE_LEFT)
                        # 待機（リスポーン時）
                        elif self.prev_key_event is KeyEvent.IDLE:
                            self.y -= 1
                        # 落下
                        elif self.prev_key_event is KeyEvent.FALL:
                            self.y -= 1
                            self.is_fixed = True

                        self.Update()
                        return

                    else:
                        self._field[y][x] = 9

        # 壁蹴りでテトリミノが一定回数持ち上げられたらテトリミノ固定猶予時間を消滅させる
        if self._adjust_pattern[max(0, self._rotate_adjust_cnt - 1)][1] < 0:
            self._rotate_adjust_cnt = 0
            self._fix_duration_cnt -= 1


    def move_right(self):
        """ 右移動 """
        self.x += 1
        self.prev_key_event = KeyEvent.MOVE_RIGHT

    def move_left(self):
        """ 左移動 """
        self.x -= 1
        self.prev_key_event = KeyEvent.MOVE_LEFT

    def fall(self):
        """ 落下 """
        self.y += 1
        self.prev_key_event = KeyEvent.FALL

        if self._fix_duration_cnt <= 0:
            self.y += 1
            self.Update()
            if not self.is_fixed:
                self.y -= 1
                self.Update()


    def hard_drop(self):
        """ ハードドロップ """
        while not self.is_fixed:
            self.fall()
            self.Update()


    def rotate_right(self):
        """ 右回転 """
        self.backup_position()
        self._rotate_adjust_cnt = 0

        _tmp = [[0, 0, 0, 0, 0] for _ in range(5)]
        for x in range(5):
            for y in range(5):
                _tmp[y][x] = self._mino_field[4 - x][y]

        self._mino_field = _tmp
        self.prev_key_event = KeyEvent.ROTATE_RIGHT

    def rotate_left(self):
        """ 左回転 """
        self.backup_position()
        self._rotate_adjust_cnt = 0

        _tmp = [[0, 0, 0, 0, 0] for _ in range(5)]
        for x in range(5):
            for y in range(5):
                _tmp[y][x] = self._mino_field[x][4 - y]

        self._mino_field = _tmp
        self.prev_key_event = KeyEvent.ROTATE_LEFT

    def fix(self):
        """ テトリミノ固定化メソッド

        固定化フラグはこのメソッドの前に立つ。操作中テトリミノを示すフィールドID値を固定後のIDに置き換える
        """
        for i, x in zip(range(5), range(self.x - 2, self.x + 3)):
            for j, y in zip(range(5), range(self.y - 2, self.y + 3)):
                if self._mino_field[j][i] != 0:
                    self._field[y][x] = self.id

    def backup_position(self):
        """ 現在の座標とテトリミノフィールド情報を保持 """
        self._prev_x = self.x
        self._prev_y = self.y
        self._prev_mino_field = copy.copy(self._mino_field)

    def rollback_position(self):
        """ 保持していた座標とテトリミノフィールド情報でロールバック """
        self.x = self._prev_x
        self.y = self._prev_y
        self._mino_field = self._prev_mino_field

    def rotate_adjust(self, rotate_event:KeyEvent):
        """ 回転の壁蹴り座標補正

        Args:
            rotate_event (KeyEvent): 回転方向
        """
        if self._rotate_adjust_cnt < len(self._adjust_pattern):
            self.x = self._prev_x + (self._adjust_pattern[self._rotate_adjust_cnt][0] *
                                     (1 if rotate_event is KeyEvent.ROTATE_RIGHT else -1))
            self.y = self._prev_y + self._adjust_pattern[self._rotate_adjust_cnt][1]

            self._rotate_adjust_cnt += 1
        else:
            self._rotate_adjust_cnt = 0
            self.rollback_position()

    @property
    def mino_field(self):
        """ テトリミノのフィールド情報を取得するプロパティ

        Returns:
            5x5のテトリミノフィールド情報を返却
        """
        return self._mino_field

    def init_mino_rotation(self):
        self._mino_field = self._initial_field
        self.Update()

