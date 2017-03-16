#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple, lightweight, WSGI-compatible web framework.
"""

__author__ = 'Qianfeng'

import types, os, sys, time, datetime, functools, re
import cgi, mimetypes, threading, urllib, traceback


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


# thread local object for storing request and response.
ctx = threading.local()


# Dict object
class Dict(dict):
    def __init__(self, names=(), values=(), **kwargs):
        super(Dict, self).__init__(**kwargs)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


_TIMEDELTA_ZERO = datetime.timedelta(0)

# timezone as UTC+8:00, UTC-10:00
_RE_TZ = re.compile('^([\+\-])([0-9]{1,2})\:([0-9]{1,2})$')


class UTC(datetime.utcinfo):
    pass


_RESPONSE_STATUS = {}

_RE_RESPONSE_STATUS = re.compile(r'^\d\d\d(\ [\w\ ]+)?$')

_RESPONSE_HEADERS = ()

_RESPONSE_HEADER_DICT = dict(zip(map(lambda x: x.upper(), _RESPONSE_HEADERS), _RESPONSE_HEADERS))

_HEADER_X_POWERED_BY = ('X-Powered-By', 'transwarp/1.0')


class HttpError(Exception):
    pass


class RedirectError(HttpError):
    pass


def badrequest():
    pass


def unauthorized():
    pass


def forbidden():
    pass


def notfound():
    pass


def conflict():
    pass


def internalerror():
    pass


def redirect(location):
    pass


def found(location):
    pass


def seeother(location):
    pass


def _to_str(s):
    pass


def _to_unicode(s, encoding='utf-8'):
    pass


def _quote(s, encoding='utf-8'):
    pass


def _unquote(s, encoding='utf-8'):
    pass


def get(path):
    pass


def post(path):
    pass


_re_route = re.compile(r'(\:[a-zA-Z_]\w*)')


def _build_regex(path):
    pass


class Route(object):
    pass


class StaticFileRoute(object):
    pass


def favicon_handler():
    pass


class MultiparFile(object):
    pass


class Request(object):
    pass


UTC_0 = UTC('+00:00')


class Response(object):
    pass


class Template(object):
    pass


class TemplateEngine(object):
    pass


class Jinja2TemplateEngine(TemplateEngine):
    pass


def _default_error_handler(e, start_response, is_debug):
    pass


def view(path):
    pass


_RE_INTERCEPTROR_STARTS_WITH = re.compile(r'^([^\*\?]+)\*?$')
_RE_INTERCEPTROR_ENDS_WITH = re.compile(r'^\*([^\*\?]+)$')


def _build_pattern_fn(pattern):
    pass


def interceptor(patttern='/'):
    pass


def _build_interceptor_chain(last_fn, *interceptor):
    pass


def _load_module(module_name):
    pass


class WSGIApplication(object):
    pass

































