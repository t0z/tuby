try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

import socket

ADDR = ('127.0.0.1', 34600)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDR)
for data in TUBY.stdin:
    s.send(data)
data = s.recv(1024)
s.close()
TUBY.stdout.write(data)
