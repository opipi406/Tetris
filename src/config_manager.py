import os, pathlib, configparser, sys
from src.utils.utils import Utils


class ConfigManager:
    """ コンフィグデータ管理クラス

    .. csv-table:: GAMEセクション
        :header: オプション, 概要
        :widths: 10, 85

        refresh_ms,  メインループの間隔（ms）
        enable_next, 次に生成されるブロック（Nextテトリミノ）表示の有効化
    """

    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__config.read('config.ini', encoding='utf-8')

        self.GAME: ConfigManager.__GAME = ConfigManager.__GAME(self.__config)


    def initialized(self, is_rebuild=False):
        """ config.iniの初期化

        Args:
            is_rebuild (bool): config.iniを削除してから初期化する
        """
        if is_rebuild and os.path.exists('config.ini'):
            os.remove('config.ini')
            pathlib.Path('config.ini').touch()
            self.__init__()

        self.GAME.initialized()


    class __Section:
        """ セクションクラス """

        def __init__(self, _config):
            self._config : configparser.ConfigParser = _config
            self._section_name = ''

        def initialized(self):
            """ 初期化 """
            if not self._config.has_section(self._section_name):
                self._config.add_section(self._section_name)

        def _get(self, section, option, return_type, default):
            """ コンフィグ値の取得

            Args:
                section: セクション
                option: オプション
                return_type: 返却される型
                default: デフォルト値
            """
            try:
                if return_type is bool:
                    return Utils.convert_bool(self._config.get(section, option), ignore_to_str=True)
                return return_type(self._config.get(section, option))
            # セクション見つからないエラー
            except configparser.NoSectionError:
                print('config.ini : [{}] is not found.'.format(section))
            # オプション見つからないエラー
            except configparser.NoOptionError:
                print('config.ini : [{}] -> "{}" is not found.'.format(section, option))
            # 全ての例外
            except Exception as e:
                print('config.ini -> {}'.format(e))
            return default  # デフォルト値を返す

        def _set(self, section, option, value):
            """ コンフィグ値の代入

            Args:
                section: セクション
                option: オプション
                value: 代入値
            """
            try:
                self._config.set(section, option, str(value))
                with open('config.ini', 'w', encoding='utf-8') as f:
                    self._config.write(f)
            # セクション見つからないエラー
            except configparser.NoSectionError:
                print('config.ini : [{}] is not found.'.format(section))
            # オプション見つからないエラー
            except configparser.NoOptionError:
                print('config.ini : [{}] -> "{}" is not found.'.format(section, option))
            # 全ての例外
            except Exception as e:
                print('config.ini -> {}'.format(e))


    # ====================================================
    #   GAME セクション
    # ====================================================
    class __GAME(__Section):
        def __init__(self, _config):
            super().__init__(_config)
            self._section_name = 'GAME'

        def initialized(self):
            super().initialized()
            self.refresh_ms = self.refresh_ms
            self.enable_next = self.enable_next

        # メインループの間隔（ms）
        @property
        def refresh_ms(self):
            return self._get(self._section_name, sys._getframe().f_code.co_name, int, 1000)
        @refresh_ms.setter
        def refresh_ms(self, v):
            self._set(self._section_name, sys._getframe().f_code.co_name, v)

        # 次に生成されるブロック（Nextテトリミノ）表示の有効化
        @property
        def enable_next(self):
            return self._get(self._section_name, sys._getframe().f_code.co_name, bool, True)
        @enable_next.setter
        def enable_next(self, v):
            self._set(self._section_name, sys._getframe().f_code.co_name, v)


config = ConfigManager()