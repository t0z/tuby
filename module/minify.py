try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()
from tuby.mini import mini

TUBY.stdout.write(mini(''.join(l for l in TUBY.stdin)))
