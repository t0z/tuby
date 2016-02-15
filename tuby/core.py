from os import path as Path, walk
import sys
import urllib
import bz2
import base64
import logging

__version__ = '0.1'
__progname__ = 'tuby'
__description__ = 'pipe python snippet'
__author__ = 't0z'
__email__ = 't0z'
__update_urls__ = [
    ('armored', 'http://localhost:5000/tuby/%s'),
    ('raw', 'https://raw.githubusercontent.com/t0z/tuby/master/module/%s.py',),
]

logging.basicConfig()
log = logging.getLogger('tuby')
log.setLevel(logging.ERROR)

try:
    __file__
except:
    __file__ = Path.expanduser('~')  # @ReservedAssignment

basepath = Path.abspath(Path.join(Path.dirname(__file__), Path.pardir))
modpath = Path.join(basepath, 'module')


def readfile(path):
    with open(path, 'rb') as io:
        return ''.join([line for line in io])


def module_list(path):
    for dirpath, _dirnames, filenames in walk(path):
        for name in filenames:
            if not name.endswith('.py'):
                continue
            yield Path.join(dirpath, name)


def _mkmodfn(name):
    return Path.join(modpath, '%s.py' % name)


def get_ssl_context():
    try:
        import ssl
        ctx = ssl.SSLContext(ssl.CERT_OPTIONAL)
        log.info('SSL context created')
        return ctx
    except Exception as e:
        log.error('- SSL certificate error: %s', e)
    return None


def GET(url, data=None):
    log.debug('url: %s', url)
    rh = urllib.urlopen(url, data, context=get_ssl_context())
    if rh.code != 200:
        log.error("HTTP error: %s", rh.code)
    else:
        for line in rh:
            yield line.decode('utf8', errors="ignore")


class Unbuffered(object):

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


class Streams(object):

    def __init__(self, stdin=None, names=['stdin', 'stdout', 'stderr'],
                 debug=True):
        self.debug = debug
        for name in names:
            setattr(self, name, Unbuffered(getattr(sys, name)))
        if stdin is not None:
            self.stdin = stdin

    def log(self, *a):
        if not self.debug:
            return
        if len(a) > 1:
            self.stderr.write(a[0] % a[1:] + '\n')
        else:
            self.stderr.write(a[0] + '\n')


class Cache(dict):
    pass


class ModuleLoader(object):

    class Site(object):

        @classmethod
        def update(cls, name):
            for kind, url in __update_urls__:
                data = ''.join([l for l in GET(url % name)])
                if data is not None:
                    if kind == 'armored':
                        data = bz2.decompress(base64.b64decode(data))
                    else:
                        data = compile(data, '<string>', 'exec')
                    return data
            return None

        @classmethod
        def local(cls, name):
            path = _mkmodfn(name)
            if not Path.exists(path):
                return None
            return compile(readfile(_mkmodfn(name)), '<string>', 'exec')

    def __init__(self, debug=True):
        self.cache = Cache()
        self.debug = True
        self.stores = [self.Site.local, self.Site.update]

    def exists(self, name):
        if name in self.cache:
            return True
        if Path.exists(_mkmodfn(name)):
            return True
        return False

    def load(self, name):
        log.info('+ Loading module: %s' % name)
        source = None
        if name in self.cache:
            return self.cache[name]
        for code in self.stores:
            source = code(name)
            if source is not None:
                return source
        return None

    def execute(self, name, stdin=None):
        if not self.exists(name):
            content = self.load(name)
            if content is None:
                raise RuntimeError('Module not found: %s' % _mkmodfn(name))
        else:
            content = self.load(name)
        local = {'TUBY': Streams(debug=self.debug)}
        if stdin is not None:
            local['TUBY'].stdin = stdin
        try:
            exec content in local
        except Exception as e:
            log.error("Error: %s", e)
        return local


def main(name='tb-list', stdin=None, debug=False):
    argv = []
    if debug is True:
        log.setLevel(logging.DEBUG)
    try:
        argv.extend(sys.argv)
    except:
        argv.append(Path.expanduser('~'))
    if stdin is None:
        stdin = sys.stdin
    modname = 'tb-help'
    log.debug('argv: %s', argv)
    numarg = len(argv)
    if numarg > 1:
        modname = argv[1]
    if numarg > 2:
        if argv[2] != '-':
            stdin = open(argv[2], 'rb')
    modname = modname.replace('-', '_')
    ml = ModuleLoader(debug=debug)
    result = ml.execute(modname, stdin=stdin)
    return result

if __name__ == '__main__':
    main(debug=True)
