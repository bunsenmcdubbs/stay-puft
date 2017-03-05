import pymysql
import json

_connection = None

def _create_connection(**kwargs):
    kwargs['cursorclass'] = pymysql.cursors.DictCursor
    connection = pymysql.connect(**kwargs)
    return connection

def get_conn(config=None):
    global _connection
    if _connection is None or _connection.open is False:
        if config is None:
            config = read_config()
        _connection = _create_connection(**config)
    return _connection

def read_config(filepath=None):
    if filepath is None:
        filepath = '../../config.json'
    with open(filepath, 'r') as raw_config:
        mysql_config = json.loads(raw_config.read())['mysql']
        return mysql_config
