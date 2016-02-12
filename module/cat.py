try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

[TUBY.stdout.write(line) for line in TUBY.stdin]
