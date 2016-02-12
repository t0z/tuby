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
    
    
# the public network interface
HOST = socket.gethostbyname(socket.gethostname())

# create a raw socket and bind it to the public interface
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind((HOST, 0))

# Include IP headers
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# receive all packages
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# receive a package
print s.recvfrom(65565)

# disabled promiscuous mode
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
'''

protos = {
    'icmp': socket.IPPROTO_ICMP,
    'icmp6': socket.IPPROTO_ICMPV6,
    'tcp': socket.IPPROTO_TCP,
    'udp': socket.IPPROTO_UDP,
}
# create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, protos['icmp'])
    # s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
except socket.error, msg:
    TUBY.log('Exception: Socket could not be created. Error Code : ' +
             str(msg[0]) + ' Message ' + msg[1])
    sys.exit(1)

# receive a packet
soread_max = 65535  # 65565
while True:
    TUBY.stdout.write(base64.b64encode(s.recvfrom(65565)[0].strip()) + '\n')
