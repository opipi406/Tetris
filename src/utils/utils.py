import os, time, stat, shutil, re
from chardet import UniversalDetector


class Utils:
    """ ユーティリティクラス """

    @staticmethod
    def clamp(x, min_value, max_value):
        """ クランプ関数

        Args:
            x: 対象の値
            min_value: 最小値
            max_value: 最大値

        Returns:
            引数xの値を[min_value]〜[max_value]の範囲内にクランプして返却
        """
        return min(max_value, max(x, min_value))

    @staticmethod
    def convert_bool(var, ignore_to_str=False, ignore_to_bool=False):
        """ bool型とstr型の相互変換を行います

        文字列から論理型への変換::

            'True', 'TRUE', 'true' → True (bool)
            それ以外の文字列 → False (bool)

        論理型から文字列への変換::

            True (bool) → 'True' (str)
            False (bool) → 'False' (str)

        Args:
            var: 変換したい値
            ignore_to_str: bool型 → str型への変換を除外する（未指定だと除外しない）
            ignore_to_bool: str型 → bool型への変換を除外する（未指定だと除外しない）

        Returns:
            | 変換対象がbool型の場合：str型で'True'か'False'を返却
            | 変換対象がstr型の場合：文字列が'True'か'true'のときはbool型でTrueを返し、それ以外の場合はFalseを返却
        """
        if ignore_to_str and type(var) is bool: return var
        elif ignore_to_bool and type(var) is str: return var

        if type(var) is str:
            var = var.lower()
            if var == 'true':
                return True
            else:
                return False

        elif type(var) is bool:
            return str(var)


    @staticmethod
    def __del_rw(action, name, exc):
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)

    @staticmethod
    def rm(path):
        """ ディレクトリ・ファイルの削除

        Args:
            path: 削除対象のパス

        Returns:
            int: 成功時は0、失敗時は-1を返却
        """
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path, onerror=Utils.__del_rw)
            elif os.path.isfile(path):
                os.remove(path)
            else:
                print('ERROR DELETE : %s' % path)
                return -1
            print('DELETE : %s' % path)
            return 0
        else:
            print('DELETE NOT FOUND : %s' % path)
            return 0

    @staticmethod
    def copy(origin_path, dest_path, is_overwrite=False):
        """ ディレクトリ・ファイルのコピー

        Args:
            origin_path: コピー元パス
            dest_path: コピー先パス
            is_overwrite: コピー先のディレクトリが既に存在していた場合も強制的に上書きコピーする

        Returns:
            int: 成功時は0、失敗時は-1を返却
        """
        if os.path.exists(origin_path):
            if os.path.exists(dest_path):
                if is_overwrite:
                    Utils.rm(dest_path)
                else:
                    print('COPY ALREADY EXIST : %s' % dest_path)
                    return 0

            if os.path.isdir(origin_path):
                shutil.copytree(origin_path, dest_path)
            elif os.path.isfile(origin_path):
                shutil.copy(origin_path, dest_path)
            else:
                print('ERROR COPY : %s' % origin_path)
                return -1
            print('COPY : %s --> %s' % (origin_path, dest_path))
            return 0
        else:
            print('COPY NOT FOUND : %s' % origin_path)
            return 0


    @staticmethod
    def check_encoding(file_path):
        """ 適切な文字エンコーディングの取得

        Args:
            file_path (str): 対象のファイルパス

        Returns:
            str: 'shift-jis' か 'utf-8' を返す
        """

        detector = UniversalDetector()
        try:
            with open(file_path, mode='rb') as f:
                for binary in f:
                    detector.feed(binary)
                    if detector.done:
                        break
        except Exception as e:
            # print(e)
            return 'shift-jis'
        finally:
            detector.close()

        _result: str = detector.result['encoding']

        if _result is None or _result.lower() == 'shift_jis':
            return 'shift_jis'
        else:
            return 'utf-8'
