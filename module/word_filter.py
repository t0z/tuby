try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

DEBUG = False
lf = '\n'


def sd(*a):
    if DEBUG:
        s(*a)


def s(*a):
    if len(a) > 1:
        TUBY.stdout.write(a[0] % a[1:] + lf)
    else:
        TUBY.stdout.write(a[0] + lf)

final = {}
threasold = 2
for data in TUBY.stdin:
    word = None
    count = None
    try:
        data = data.decode('utf8', errors='replace').strip()
        count, word = data.split(' ', 1)
        count = int(count)
    except Exception as e:
        sd('Exception: %s\n\t%s' % (e, data))
        continue
    if word not in final:
        final[word] = count
    else:
        final[word] += count

for k in final.keys():
    TUBY.stdout.write(u'%s: %s\n' % (k, final[k]))
