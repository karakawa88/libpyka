"""libpykaライブラリのutilsモジュールのテスト
"""

from typing import Optional, Union, Any
from typing import Callable, NoReturn
from typing import Sequence, Iterable, List, Tuple
from typing import Dict
from typing import TypeVar, Generic, NewType, Type

import unittest
from pathlib import Path
from libpyka.utils import bytes_enc
from libpyka.utils import hashint, hashint64

class BytesEncTest(unittest.TestCase):
    """libpykaライブラリのbytes_enc()関数のテスト
    バイトの文字列から文字コードを認識できるかテストする。
    """
    
    def test_bytes_enc_utf8(self):
        """このファイルを元にUTF-8を認識できるかテストする
        Raises:
            AssertionError:  このファイルをUTF-8と認識できない
        """
        fname = Path(__file__)
        byte_content = fname.read_bytes()
        enc = bytes_enc(byte_content)
        self.assertEqual('utf-8', enc)

    def test_bytes_enc_shift_jis(self):
        """Shift_JIS文字コードのファイルで認識できるかテストする
        Raises:
            AssertionError:  ファイルをShift_JISと認識できない
        """
        fname = 'data/test_utils.py.shift_jis'
        path = Path('tests') / fname
        byte_content = path.read_bytes()
        enc = bytes_enc(byte_content)
        self.assertEqual('shift_jis', enc.lower() if enc is not None else enc)

    def test_bytes_enc_none(self):
        """文字コードを認識できない場合はNoneを返すかテストする
        Raises:
            AssertionError:  文字コードを認識できない場合Noneを返さない
        """
        fname = 'data/logo.png'
        path = Path('tests') / fname
        byte_content = path.read_bytes()
        enc = bytes_enc(byte_content)
        self.assertIsNone(enc)

class HashIntTest(unittest.TestCase):
    """libpykaライブラリのhashint**()関数のテスト
    ハッシュがちゃんと生成できるかテストする。
    """

    def read_bytes(self, fname: Path) -> bytes:
        """ファイルの内容のバイト列を返す
        Args:
            path (str): ファイル名
        Returns:
            bytes: ファイルの内容
        Raises:
            FileNotFoundError: ファイルが存在しない
        """

    def test_hash_int_equal(self):
        """hashint()関数が同じファイルで同じハッシュ関数を生成するかテスト
        Raises:
            AssertionError: 同じ内容でハッシュが同じものでない
        """
        fname = 'data/logo.png'
        path = Path('tests') / fname
        byte_content = path.read_bytes()
        hash1 = hashint(byte_content)
        hash2 = hashint(byte_content)
        self.assertEqual(hash1, hash2)

    def test_hash_int_sha256sum_equal(self):
        """libpykaライブラリのhashint()関数の生成するハッシュと
        シェルのsha256sum関数が生成するハッシュで同じ
        整数値が生成できるかテストする。
        """
        fname = 'data/logo.png'
        path = Path('tests') / fname
        
