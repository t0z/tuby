from os import path as Path
from flask import Flask
from flask import request, Response
import logging
from tuby.core import modpath, readfile, basepath
from tuby.mini import mini

logging.basicConfig()
log = logging.getLogger('tubyd')
log.setLevel(logging.DEBUG)

app = Flask(__name__)
methods = ['GET', 'POST']
debug = True

log.debug('listening on %s:%s', app.config.get('host'), app.config.get('port'))

MIME_RESPONSE = 'application/json'


class Err(object):

    file_not_found = ('File not found', 404)


@app.route('/tuby', methods=methods)
def serv_tuby():
        path = Path.join(basepath, 'tuby', 'core.py')
        if Path.exists(path):
            return Response(mini(readfile(path)), mimetype=MIME_RESPONSE)
        return Err.file_not_found, 404


@app.route('/<modname>', methods=methods)
def serv_module(modname):
    modname = modname.decode('utf8').strip().replace(u'.', u'_')
    log.debug('%s: %s', request.method, modname)
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


def gen_ssl_context(path='../data'):
    return None
    path = Path.abspath(path)
    ctx = []
    for filename in ['cert.crt', 'key.key']:
        fpath = Path.join(path, filename)
        if not Path.exists(fpath):
            print('file not found: %s' % fpath)
            return None
        ctx.append(fpath)
    return ctx

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=debug, ssl_context=gen_ssl_context())
