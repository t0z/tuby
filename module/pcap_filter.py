import socket
from struct import unpack
import base64
from multiprocessing import Pool
from multiprocessing import log_to_stderr

"""
   from: http://www.binarytides.com/python-packet-sniffer-code-linux/
"""

__pool_worker__ = 3

try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

pool = Pool(__pool_worker__)


def analyze(packet):

    # take first 20 characters for the ip header
    ip_header = packet[0:20]

    # now unpack them :)
    iph = unpack('!BBHHHBBH4s4s', ip_header)

    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF

    iph_length = ihl * 4

    ttl = iph[5]
    protocol = iph[6]
    s_addr = socket.inet_ntoa(iph[8])
    d_addr = socket.inet_ntoa(iph[9])
    tcp_header = packet[iph_length:iph_length + 20]

    # now unpack them :)
    tcph = unpack('!HHLLBBHHH', tcp_header)

    s_port = tcph[0]
    d_port = tcph[1]
    _sequence = tcph[2]
    _acknowledgement = tcph[3]
    doff_reserved = tcph[4]
    tcph_length = doff_reserved >> 4
    h_size = iph_length + tcph_length * 4
    _data_size = len(packet) - h_size

    # get data from the packet
    _data = packet[h_size:]

    TUBY.stdout.write('%s#%s#%s#%s#%s#%s#%s\n' % (version, ttl, protocol,
                                                  s_addr, s_port, d_addr,
                                                  d_port))
"""Main"""
log_to_stderr()
queue = []
for packet in TUBY.stdin:
    if packet is None:
        continue
    packet = packet.strip()
    if packet == '':
        continue
    try:
        analyze(base64.b64decode(packet))
    except Exception as e:
        print(" Error: %s", e)
