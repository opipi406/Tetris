""" 定数モジュール """

WINDOW_WIDTH = 600
""" ウィンドウ横幅 """
WINDOW_HEIGHT = 700
""" ウィンドウ縦幅 """

BLOCK_SIZE = 28
""" フィールドブロックの縦横サイズ（px） """

FIELD_BLOCK_X = 10
""" テトリスフィールドの横ブロック数 """
FIELD_BLOCK_Y = 24
""" テトリスフィールドの縦ブロック数 """
FIELD_BLOCK_OVER_Y = 4
""" テトリスフィールド上部画面外の縦ブロック数 """

INITIAL_MINO_X = 4
""" テトリミノ初期x座標 """
INITIAL_MINO_Y = 1 + FIELD_BLOCK_OVER_Y
""" テトリミノ初期y座標 """

SCORE_RATE = (40, 100, 300, 1200)
""" スコアレート（シングル, ダブル, トリプル, テトリス） """

FONT = ('Courier', '18')
""" フォント """

TEXT_SCORE = 'SCORE  {:0>8}'
""" 獲得スコアのテキストフォーマット """
TEXT_LINES = 'LINES  {:0>8}'
""" 消去ライン数のテキストフォーマット """
TEXT_PIECES = 'PIECES {:0>8}'
""" 生成テトリミノ数のテキストフォーマット """
TEXT_EPISODES = 'EPISODES {:0>8}'
""" エピソード数のテキストフォーマット """

MINO_I_ID = 1
""" I字ミノの識別ID """
MINO_J_ID = 2
""" J字ミノの識別ID """
MINO_L_ID = 3
""" L字ミノの識別ID """
MINO_O_ID = 4
""" O字ミノの識別ID """
MINO_S_ID = 5
""" S字ミノの識別ID """
MINO_T_ID = 6
""" T字ミノの識別ID """
MINO_Z_ID = 7
""" Z字ミノの識別ID """
