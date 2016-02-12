try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

import socket
import sys
import base64

'''
    from: http://www.binarytides.com/python-packet-sniffer-code-linux/
'''

# create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error, msg:
    TUBY.log('Exception: Socket could not be created. Error Code : ' +
             str(msg[0]) + ' Message ' + msg[1])
    sys.exit(1)

# receive a packet
soread_max = 65535  # 65565
while True:
    TUBY.stdout.write(base64.b64encode(s.recvfrom(65565)[0].strip()) + '\n')
