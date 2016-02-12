try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

for line in TUBY.stdin:
    line = line.rstrip()
    if line == '':
        continue
    if line.startswith('#'):
        continue
    TUBY.stdout.write(line + '\n')
