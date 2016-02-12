from tuby.core import TubyStream
try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    TUBY = TubyStream()

import os
from tuby.core import modpath, readfile, _mkmodfn

for dirpath, dirnames, filenames in os.walk(modpath):
    for fn in filenames:
        if not fn.endswith('.py'):
            continue
        if fn.startswith('tb_module_manifest'):  # infinite loop
            continue
        module = compile(
            ''.join(readfile(_mkmodfn(fn[:-3]))), '<string>', 'exec')
        scope = {'TUBY': TubyStream()}
        try:
            exec module in scope
        except Exception:
            pass

        def getvalue(key):
            if key not in scope['TUBY']:
                return 'na'
            return scope['TUBY'][key].encode('utf8')
        version = getvalue('__version__')
        author = getvalue('__author__')
        email = getvalue('__email__')
        msg = '%s %s\n' % (version, fn[:-3], author, email)
        TUBY.stdout.write(msg)
