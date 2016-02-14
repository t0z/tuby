try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

import socket

ADDR = ('0.0.0.0', 34600)  # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)
s.listen(1)
while True:
    conn, addr = s.accept()
    TUBY.stdout.write(u'client connected: %s\n' % str(addr))
    data = ''
    while True:
        data += conn.recv(1024)
        if not data:
            conn.close()
            print(u'+ client disconnected: %s' % str(addr))
            break
#         if not data.find('\n'):
#             continue
        TUBY.stdout.write(data + '\n')
        data = ''
    TUBY.stdout.write(data + '\n')
    conn.close()
s.close()
