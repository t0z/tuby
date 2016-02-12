try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

import urllib
import sys

data = None
urls = ''

if len(sys.argv) > 3:
    urls = sys.argv[3]
else:
    urls = u''.join([l.encode('utf8') for l in TUBY.stdin]).strip()
if len(sys.argv) > 4:
    data = u' '.join(sys.argv[3:].encode('utf8'))
urls = urls.split('\n')
for url in urls:
    rh = urllib.urlopen(url, data)
    for line in rh:
        TUBY.stdout.write(line.decode('utf8', errors="ignore"))
