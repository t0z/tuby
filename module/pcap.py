# http://www.binarytides.com/python-packet-sniffer-code-linux/

import socket
import sys
import base64
TUBY = TUBY  # @UndefinedVariable

# create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error, msg:
    print 'Socket could not be created. Error Code : '\
        + str(msg[0]) + ' Message ' + msg[1]
    sys.exit(1)

# receive a packet
soread_max = 65535  # 65565
while True:
    TUBY.stdout.write(base64.b64encode(s.recvfrom(65565)[0].strip()) + '\n')
    TUBY.stdout.flush()
