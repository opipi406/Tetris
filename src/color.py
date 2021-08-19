
class Color:
    """ カラーコードクラス """

    GRAY        = '#d2d2d2' # グレー
    CYAN        = '#00e0e0' # シアン
    BLUE        = '#0000ff' # 青
    ORANGE      = '#ff9300' # オレンジ
    YELLOW      = '#ffe32a' # 黄
    GREEN       = '#00ff00' # 緑
    PURPLE      = '#d400ff' # 紫
    RED         = '#ff0000' # 赤
    DEEP_GRAY   = '#777777' # 濃いグレー

    @staticmethod
    def ID(_id):
        colors = [
            Color.GRAY,
            Color.CYAN,
            Color.BLUE,
            Color.ORANGE,
            Color.YELLOW,
            Color.GREEN,
            Color.PURPLE,
            Color.RED,
        ]
        return colors[_id] if 0 <= _id < len(colors) else Color.DEEP_GRAY