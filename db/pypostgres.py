import psycopg2
import configparser
import sys
import logging
import re
from db import SQLException

###
# @brief DB PostgreSQLに関連するユティリティーモジュール。
#

#ロガー
logger: logging.Logger = logging.getLogger('postgres')

##
# @brief DBに接続し、接続オブジェクトを返す。
# 
# DBはPostgreSQLでコネクターはpsycopg2を使用している。
# @param host       ホスト名
# @param port       ポート番号
# @param user       ユーザー名
# @param password   パスワード
# @param dbname     DB名
# @return DBコネクションオブジェクト
# @exception psycopg2.Error   DB接続エラー
def get_connection(host: str='localhost', port: int=5432, user: str=None, password: str=None,
        dbname: str="db1") -> psycopg.connection:
    connect_str = "host={host} port={port} user={user} password={password} dbname={dbname}"
    connect_str = connect_str.format(host=host, port=port, 
                        user=user, password=password, dbname=dbname)
    dbcon = None
    try:
        mess = re.sub('password=(.*?) ', 'password=******', connect_str)
        logger.info('PostgreSQL接続情報 ' + mess)
        dbcon = psycopg2.connect(connect_str)
    except psycopg2.Error as ex:
        logger.error('DB接続時にエラー: ', mess, file=sys.stderr)
        raise SQLException('DB接続時にエラー 接続文字列: ' + mess, ex)
    return dbcon


##
# @brief ini設定ファイルを読み込みそのパラメーターを元にDBに接続し、
#       コネクションオブジェクトを返す。
# iniファイルの形式
# [postgres]  #セクション名は引数で指定可能
#   host=ホスト名
#   port=ポート番号
#   user=ユーザー名
#   password=パスワード
#   dbname=DB名
# ユーザー名パスワードは必ず設定する必要がある。
# DBはPostgreSQLでコネクターはpsycopg2を使用している。
# @param inifile ini設定ファイル
# @param section セクション名
# @return DBコネクションオブジェクト
# @exception psycopg2.Error   DB接続エラー
def get_config_connection(inifile: str, section: str='PostgreSQL') -> psycopg.connection:
    logger.debug(f'DB接続iniファイル inifile={inifile}, section={section}')
    config = configparser.ConfigParser()
    config.read(inifile)
    params = {}
    if config.has_option(section, 'host'):
        params['host'] = config.get(section, 'host')
    if config.has_option(section, 'port'):
        params['port'] = config.get(section, 'port')
    if config.has_option(section, 'dbname'):
        params['dbname'] = config.get(section, 'dbname')
    params['user'] = config.get(section, 'user')
    params['password'] = config.get(section, 'password')
    dbcon = get_connection(**params)
    return dbcon

# *importでimportするクラス・関数
__all__ = ['get_connection', 'get_config_connection']
