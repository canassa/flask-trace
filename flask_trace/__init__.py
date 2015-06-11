# coding: utf-8

from __future__ import absolute_import
from functools import wraps
import inspect
import logging
import repr as reprlib
import sys
import uuid

__version__ = '0.0.3'
__all__ = ('get_log_id', 'trace', 'Formatter')


LOG_TRACE = 15
logging.addLevelName(LOG_TRACE, "TRACE")


logrepr = reprlib.Repr()
logrepr.maxarray = 10
logrepr.maxdict = 20
logrepr.maxstring = 50


def get_log_id():
    from flask import g

    if not hasattr(g, 'trace_uuid'):
        g.trace_uuid = str(uuid.uuid4())

    return g.trace_uuid


def trace(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        logargs = []
        for k, v in inspect.getcallargs(f, *args, **kwargs).items():
            if k == 'self':
                continue
            elif k == 'password':
                v = '******'
            else:
                v = logrepr.repr(v).replace('"', "'")

            logargs.append(u'{0}="{1}"'.format(k, v))

        extra = {
            'trace_pathname': inspect.getfile(f)
        }

        try:
            extra.update({'trace_lineno': inspect.getsourcelines(f)[1]})
        except IndexError:
            pass

        try:
            from flask import current_app

            current_app.logger.trace(u'func_name=%s %s', f.func_name, ' '.join(logargs), extra=extra)
        except RuntimeError:
            # Just in case we are working outside the application context and
            # the current_app is not available
            pass

        return f(*args, **kwargs)

    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__

    return wrapper


class Formatter(logging.Formatter):
    def format(self, record):
        record.message = record.getMessage()

        args = record.__dict__
        args['asctime'] = self.formatTime(record, self.datefmt)
        args['trace_uuid'] = get_log_id()

        if record.levelno == LOG_TRACE:
            args['pathname'] = args['trace_pathname']
            args['lineno'] = args['trace_lineno']

        s = '%(asctime)s %(levelname)s: trace_uuid=%(trace_uuid)s %(message)s [in %(pathname)s:%(lineno)d]' % args

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            try:
                s = s + record.exc_text
            except UnicodeError:
                # Sometimes filenames have non-ASCII chars, which can lead
                # to errors when s is Unicode and record.exc_text is str
                # See issue 8924.
                # We also use replace for when there are multiple
                # encodings, e.g. UTF-8 for the filesystem and latin-1
                # for a script. See issue 13232.
                s = s + record.exc_text.decode(sys.getfilesystemencoding(), 'replace')

        return s


logging.Logger.trace = lambda self, message, *args, **kwargs: self._log(LOG_TRACE, message, args, **kwargs)
