try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

import sys
import struct
import socket


def ip2int(addr):
    return int(struct.unpack("!I", socket.inet_aton(addr))[0])


def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


def genlist(src):
    iptxt, cidr = [p.strip() for p in src.split('/')]
    ipnum = ip2int(iptxt)
    rest = ~((1 << (32 - int(cidr))) - 1)
    minr = ipnum & rest
    maxr = minr ^ ~rest
    for i in range(minr, maxr):
        yield int2ip(i)


def helper(ip):
    for ip in genlist(ip):
        TUBY.stdout.write(ip + '\n')

if len(sys.argv) > 3:
    for ip in ' '.join(sys.argv[3:]).split(' '):
        helper(ip)
else:
    for src in TUBY.stdin:
        helper(ip)
