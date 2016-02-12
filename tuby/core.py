from os import path as Path, walk
import sys

__version__ = '0.1'
__progname__ = 'tuby'
__description__ = 'pipe python snippet'
__author__ = 't0z'
__email__ = 't0z'

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


class Unbuffered(object):

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


class TubyStream(object):

    def __init__(self, names=['stdin', 'stdout', 'stderr'], debug=True):
        self.debug = debug
        for name in names:
            setattr(self, name, Unbuffered(getattr(sys, name)))

    def log(self, *a):
        if not self.debug:
            return
        if len(a) > 1:
            self.stderr.write(a[0] % a[1:] + '\n')
        else:
            self.stderr.write(a[0] + '\n')


class ModuleLoader(object):

    def __init__(self, debug=True):
        self.debug = True

    def exists(self, name):
        if Path.exists(_mkmodfn(name)):
            return True
        return False

    def load(self, name):
        return compile(readfile(_mkmodfn(name)), '<string>', 'exec')

    def execute(self, name, stdin=None):
        if not self.exists(name):
            raise RuntimeError('Module not found: %s' % _mkmodfn(name))
        content = self.load(name)
        local = {'TUBY': TubyStream(debug=self.debug)}
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
