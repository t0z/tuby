try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

import os
from tuby.core import modpath

for dirpath, dirnames, filenames in os.walk(modpath):
    for fn in filenames:
        if not fn.endswith('.py'):
            continue
        fn = fn[:-3]
        TUBY.stdout.write('%s %s\n' % (dirpath, fn))
