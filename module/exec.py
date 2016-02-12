import dis
import base64
try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

exec(base64.b64decode(''.join([l.strip() for l in TUBY.stdin.])), None, TUBY)
