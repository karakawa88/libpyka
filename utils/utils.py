##
# @brief 一般的なユーティリティモジュール。
#

import hashlib

# 4バイト unsigned int の最大値
MAX_UNSIGNED_INT = 4294967295
# 8バイト unsigned long の最大値
MAX_UNSIGNED_LONG = 18446744073709551615

##
# @brief バイトコンテントから４バイトの整数のハッシュ値を生成して返す。
#
# ハッシュはSHA256を使用。
# 引数でハッシュ値の範囲を指定できる。指定できない場合は４バイト(32ビット)。
# @param byte_content バイトデーター
# @param max_range  生成されるハッシュ値の最大値
# @return 整数のハッシュ値
def hashint(byte_content: bytes, max_range: int=MAX_UNSIGNED_INT):
    ret = 1
    sha = hashlib.sha256()
    sha.update(byte_content)
    hashval = sha.hexdigest()
    for ch in hashval:
        val = ord(ch)
        ret = ret + val
    ret = ret * 1234567
    return ret % max_range

##
# @brief バイトコンテントから8バイトの整数のハッシュ値を生成して返す。
#
# @return 8バイトのハッシュ値の整数
def hashint_64(byte_content: bytes):
    return hashint(byte_content, MAX_UNSIGNED_LONG)

# *importでimportするクラス・関数
__all__ = ['MAX_UNSIGNED_INT', 'MAX_UNSIGNED_LONG', 'hashint', 'hashint_64']
