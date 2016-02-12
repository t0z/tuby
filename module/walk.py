try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()
