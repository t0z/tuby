from os import path as Path, walk
import sys
import urllib
import bz2
import base64

__version__ = '0.1'
__progname__ = 'tuby'
__description__ = 'pipe python snippet'
__author__ = 't0z'
__email__ = 't0z'
__update_urls__ = [
    ('armored', 'http://localhost:5000/%s'),
    ('raw', 'https://raw.githubusercontent.com/t0z/tuby/master/module/%s.py',),
]

if __file__ is None:
    __file__ = '__memory__'

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
        from ssl import Purpose
        ctx = ssl.SSLContext(ssl.CERT_OPTIONAL)
        return ctx
    except Exception as e:
        print('- SSL certificate error: %s' % e)
    return None


def GET(url, data=None):
    print('url: %s' % url)
    rh = urllib.urlopen(url, data, context=get_ssl_context())
    if rh.code != 200:
        print "HTTP error: %s" % rh.code
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

    def __init__(self, stdin=None, names=['stdin', 'stdout', 'stderr'], debug=True):
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
        print('name: %s' % name)
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
        local = {
            'TUBY': Streams(debug=self.debug)
        }
        if stdin is not None:
            local['TUBY'].stdin = stdin
        try:
            exec content in local
        except Exception as e:
            print "Error: %s" % e
        return local


def main(name='tb-list', stdin=None, debug=True):
    name = name.replace('-', '_')
    ml = ModuleLoader(debug=debug)
    result = ml.execute(name, stdin=stdin)
    return result

if __name__ == '__main__':
    argv = []
    argv.extend(sys.argv)
    stdin = sys.stdin
    name = 'tb-help'
    numarg = len(argv)
    if numarg > 1:
        name = sys.argv[1]
    if numarg > 2:
        if sys.argv[2] != '-':
            stdin = open(sys.argv[2], 'rb')
    try:
        main(name, stdin=stdin)
    except KeyboardInterrupt:
        print 'Got Ctrl-C, interrupting.'
    except Exception as e:
        print 'Error: %s' % e
    sys.exit(0)
