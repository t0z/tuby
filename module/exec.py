try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

local = {'TUBY': TUBY}
exec(''.join([l for l in TUBY.stdin]), local, None)
