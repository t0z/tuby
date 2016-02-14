try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import Streams
    TUBY = Streams()

import platform
import socket
import sys
import base64
import binascii

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


def raw_socket():
    """ create a raw socket"""
    sock = None
    system = platform.system().lower()
    try:
        if system == 'linux':
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                 socket.IPPROTO_TCP)
        elif system == 'windows':
            HOST = socket.gethostbyname(socket.gethostname())
            # Create a raw socket and bind it to the public interface.
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                 socket.IPPROTO_IP)
            sock.bind((HOST, 0))
            # Include IP headers
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

            # Receive all packages.
            sock.ioctl(socket.SIO_RCVALL,  # @UndefinedVariable
                       socket.RCVALL_ON)  # @UndefinedVariable
        else:
            raise RuntimeError('Unknown platform: %s', platform.system())
    except socket.error, msg:
        raise RuntimeError('Socket could not be created.'
                           '\n\tError Code : %s\n\tMessage ' %
                           (str(msg[0])), msg[1])
    # tell kernel not to put in headers, since we are provpkt_iding it
    return sock
# protos = {
#     'icmp': socket.IPPROTO_ICMP,
#     # 'icmp6': socket.IPPROTO_ICMPV6,
#     'tcp': socket.IPPROTO_TCP,
#     'udp': socket.IPPROTO_UDP,
# }
# create an INET, STREAMing socket
try:
    sock = raw_socket()
    # socket.socket(socket.AF_INET, socket.SOCK_RAW,socket.IPPROTO_TCP)
except socket.error, msg:
    TUBY.log('Exception: Socket could not be created. Error Code : ' +
             str(msg[0]) + ' Message ' + msg[1])
    sys.exit(1)

# receive a packet
while True:
    try:
#         TUBY.stdout.write(
#             base64.b64encode(
#                 sock.recvfrom(65565)[0].strip()) + '\n')
        TUBY.stdout.write(base64.b64encode(sock.recvfrom(65565)[0].strip()) + '\n')
    except KeyboardInterrupt:
        print "Ctrl-C"
        break
