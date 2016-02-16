try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream  # @UnresolvedImport
    TUBY = TubyStream()

import bz2

TUBY.stdout.write(bz2.compress(''.join([l for l in TUBY.stdin])))
