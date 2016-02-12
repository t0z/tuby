try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

import zlib

TUBY.stdout.write(zlib.compress(''.join([l for l in TUBY.stdin])))
