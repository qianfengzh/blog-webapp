#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import threading
import functools

import mysql.connector


__author__ = 'Qianfeng'

engine = None


class DBError(Exception):
    pass


class _Engine(object):

    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        return self._connect()


def create_engine(user, passwd, database, host='127.0.0.1', port=3306, **kwargs):
    global engine
    if engine is not None:
        raise DBError('Engine is already initialized.')
    params = dict(user=user, passwd=passwd, database=database, host=host, port=port)
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
    for k, v in defaults.iteritems():
        params[k] = kwargs.pop(k, v)
    params.update(defaults)
    params['buffered'] = True
    engine = _Engine(lambda: mysql.connector.connect(**params))
    logging.info('Init mysql engine <%s> ok.' % hex(id(engine)))


class _LazyConnection(object):

    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            self.connection = engine.connect()
            logging.info('open connection <%s>...' % hex(id(self.connection)))
            return self.connection.cursor()
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        if self.connection:
            self.connection.close()
            logging.info('close connection <%s>...' % hex(id(self.connection)))
            self.connection = None


class _DBConnection(threading.local):

    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return self.connection is not None

    def init(self):
        logging.info('open lazy connection...')
        self.connection = _LazyConnection()
        self.transactions = 0

    def cursor(self):
        return self.connection.cursor()

    def close(self):
        self.connection.close()
        self.connection = None

_db_connection = _DBConnection()


class _ConnectionCtx(object):
    def __enter__(self):
        global _db_connection
        self.should_close = False
        if not _db_connection.is_init():
            _db_connection.init()
            self.should_close = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _db_connection
        if self.should_close:
            _db_connection.close()


def with_connection(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        with _ConnectionCtx():
            return func(*args, **kwargs)
    return _wrapper


@with_connection
def _select(sql, first, *args):
    global _db_connection
    cursor = None
    sql = sql.replace('?', '%s')
    result = {}
    results = []
    try:
        cursor = _db_connection.cursor()
        cursor.execute(sql, args)
        if cursor.description:
            columns = [x[0] for x in cursor.description]
        if first:
            values = cursor.fetchone()
            if not values:
                return None
            for k, v in zip(columns, values):
                result[k] = v
            return result
        for value in cursor.fetchall():
            print value
            for k, v in zip(columns, value):
                result[k] = v
            results.append(result)
        return results
        # return [dict(columns, value) for value in cursor.fetchall()]
    finally:
        if cursor:
            cursor.close()


def select_one(sql, *args):
    return _select(sql, True, *args)


def select_int(sql, *args):
    d = _select(sql, False, *args)
    return d.values()[0]


def select(sql, *args):
    return _select(sql, False, *args)


@with_connection
def _update(sql, *args):
    global _db_connection
    cursor = None
    sql = sql.replace('?', '%s')
    try:
        cursor = _db_connection.cursor()
        cursor.execute(sql, args)
        r = cursor.rowcount
        if _db_connection.transactions == 0:
            _db_connection.connection.commit()
        return r
    finally:
        if cursor:
            cursor.close()


def update(sql, *args):
    return _update(sql, *args)


def insert(table, **kwargs):
    cols = kwargs.keys()
    args = kwargs.values()
    sql = 'insert into %s (%s) values (%s)' % (table, ','.join(['%s' % col for col in cols]),
                                                 ','.join(['?' for i in range(len(cols))]))
    print sql
    return _update(sql, *args)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    create_engine('root', 'password', 'blogdb')
    update('drop table if exists user')
    update('create table user (id int primary key, name text, email text, passwd text, last_modified real)')
    insert('user', id=1, name='zhangsan')
    insert('user', id=2, name='lisi')
    query_one = select_one('select id,name from user')
    query = select('select id,name from user')
    print query_one
    print query
