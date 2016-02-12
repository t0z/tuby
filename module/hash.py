try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

import sys
import hashlib

cipher = 'md5'
if len(sys.argv) > 3:
    cipher = sys.argv[3]
engine = hashlib.new(cipher, '')
for line in TUBY.stdin:
    engine.update(line)
TUBY.stdout.write(engine.hexdigest() + '\n')
