try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

import socket
from struct import unpack
from multiprocessing import Pool
from multiprocessing import log_to_stderr
from time import time


"""
   from: http://www.binarytides.com/python-packet-sniffer-code-linux/
"""

__pool_worker__ = 3


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


def itstime(timeout=1.5, created_on=time()):

    def check(reset=False, created_on=created_on):
        if reset:
            created_on = time()
        if time() - created_on > timeout:
            return True
        return False

    return check


def stats():

    class Vault():
        count = 0
        avgpps = 0

        def avg(self):
            return self.avgpps

        def add(self, pps):
            self.count += 1
            self.avgpps = (self.avgpps + pps) / 2
    return Vault()


def s(*a):
    TUBY.stdout.write(a[0] % a[1:])
    TUBY.stdout.flush()

"""Main"""
log_to_stderr()
queue = []
started_on = time()
count = 0
instpps = 0
last_on = time()
reset = ''
shoutout = itstime()
st = stats()
size = 0


def print_stat(st, reset):
    msg = '[packet] count: %s pkt, pps: %s pkt/s' %\
        (st.count, round(st.avg() / 1000))
    s(reset)
    s(msg)
    return ''.join(['\b' for _i in range(0, len(msg))])

for packet in TUBY.stdin:
    if True:  # shoutout():
        if packet is None:
            continue
    packet = packet.strip()
    if packet == '':
        continue
    count += 1
    size += len(packet)
    now = time()
    elapsed = now - last_on
    pps = 1 / elapsed
    last_on = now
    st.add(pps)
    reset = print_stat(st, reset)
