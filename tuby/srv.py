from os import path as Path
import ssl  # @UnusedImport
import logging

from flask import Flask
from flask import request, Response
from flask_restful import reqparse

from tuby.core import modpath, readfile, basepath
from tuby.mini import mini

logging.basicConfig()
log = logging.getLogger('tubyd')
log.setLevel(logging.DEBUG)

app = Flask(__name__)
methods = ['GET', 'POST']
location = ['headers', 'values', 'json']
debug = True
httpd_root_path = '/tuby'
use_ssl = False

log.debug('listening on %s:%s', app.config.get('host'), app.config.get('port'))

MIME_RESPONSE = 'application/json'


def request_parser(req):
    parser = reqparse.RequestParser(bundle_errors=True)

    def addarg(name, *a, **ka):
        parser.add_argument(name, location=location, *a, **ka)
    addarg('_', required=True)
    return parser.parse_args(req=req, strict=True)


class Err(object):

    file_not_found = ('File not found', 404)


@app.route(httpd_root_path, methods=methods)
@app.route('%s/<modname>' % httpd_root_path, methods=methods)
def serv_module(modname=None):
    log.debug('%s: %s', request.method, modname)
    if modname is None:
        args = request_parser(request)
        modname = args._
    modname = modname.decode('utf8').strip().replace(u'.', u'_')
    if modname == '_':
        path = Path.join(basepath, 'tuby', 'core.py')
        if not Path.exists(path):
            return Err.file_not_found, 404
        return Response(mini(readfile(path)), mimetype=MIME_RESPONSE)
    path = None
    for storepath in [modpath, Path.abspath(Path.join(basepath, Path.pardir,
                                                      'smodule'))]:
        path = Path.join(storepath, u'%s.py' % modname)
        if not Path.exists(path):
            continue
        content = readfile(path)
        if content is not None:
            return Response(mini(content), mimetype=MIME_RESPONSE)
    log.error('File not found: %s', path)
    return Err.file_not_found


def gen_ssl_context(path='../data/cert', use_ssl=True):
    if not use_ssl:
        return None
    path = Path.abspath(path)
    ctx = []
    for filename in ['server.crt', 'server.key']:
        fpath = Path.join(path, filename)
        if not Path.exists(fpath):
            print('file not found: %s' % fpath)
            return None
        ctx.append(fpath)
    return (ctx[0], ctx[1])

if __name__ == '__main__':
    ssl_context = gen_ssl_context(use_ssl=use_ssl)
    print "ssl context: %s" % str(ssl_context)
    app.run(host="0.0.0.0", port=5000, debug=debug)# ssl_context=ssl_context)
