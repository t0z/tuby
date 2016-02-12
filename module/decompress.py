try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()
import sys
# import zlib
import bz2
# import base64


TUBY.stdout.write(bz2.decompress(''.join([l for l in TUBY.stdin])))
