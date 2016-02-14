import socket
from struct import unpack
import base64
import json

"""
   from: http://www.binarytides.com/python-packet-sniffer-code-linux/
"""

try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import Streams
    TUBY = Streams()


class Packet(object):

    class Tcp(object):

        def __init__(self, packet):
            self.packet = packet
            self._preprocess()

        def _preprocess(self):
            version_ihl = self.packet.ip.iph[0]
            # version = version_ihl >> 4
            ihl = version_ihl & 0xF
            iph_length = ihl * 4
            # ttl = iph[5]
            # protocol = iph[6]
            # s_addr = socket.inet_ntoa(iph[8])
            # d_addr = socket.inet_ntoa(iph[9])
            tcp_header = self.packet.raw[iph_length:iph_length + 20]
            # now unpack them :)
            self.tcph = unpack('!HHLLBBHHH', tcp_header)

        def s_port(self):
            return self.tcph[0]

        def d_port(self):
            return self.tcph[1]

    class Ip(object):

        def __init__(self, packet):
            self.packet = packet
            self._preprocess()

        def _preprocess(self):
            ip_header = self.packet.raw[0:20]
            # now unpack them :)
            self.iph = unpack('!BBHHHBBH4s4s', ip_header)

        def version(self):
            return self.iph[0] >> 4

        def ttl(self):
            return self.iph[5]

        def protocol(self):
            return self.iph[6]

        def s_addr(self):
            return socket.inet_ntoa(self.iph[8])

        def d_addr(self):
            return socket.inet_ntoa(self.iph[9])

    def __init__(self, raw):
        if raw is None or len(raw) < 1:
            raise RuntimeError('Empty packet data')
        self.raw = raw
        self.ip = Packet.Ip(self)
        self.tcp = Packet.Tcp(self)
#         self._preprocess()
#         self.ip = Packet.Ip(self)
#         self.tcp = Packet.Tcp(self)
# 
#     def __getattr__(self, name):
#         if name in ['ip', 'tcp']:
#             module = getattr(Packet, ucfirst(name))(self)
#             print "module: %s" % module
#             setattr(self, name, module)
#             if not hasattr(self, name):
#                 raise RuntimeError('Attribute not set: %s', name)


def ucfirst(txt):
    if txt is None or txt == '':
        return txt
    if len(txt) < 2:
        return txt.upper()
    return txt[0].upper() + txt[1:].lower()


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

    packet = {
        'version': version,
        'ttl': ttl,
        'protocol': protocol,
        's_addr': s_addr,
        'd_addr': d_addr,
        's_port': s_port,
        'd_port': d_port,
        'sequence': _sequence,
        '_acknoledfement': _acknowledgement,
        'tcph_length': tcph_length,
        'h_size': h_size,
        'payload': base64.b64encode(_data),
    }

    TUBY.stdout.write(json.dumps(packet) + '\n')

"""Main"""
for line in TUBY.stdin:
    pkt = None
    try:
        pkt = Packet(base64.b64decode(line.strip()))
    except Exception as e:
        print('Error: %s' % e)
        continue
    TUBY.stdout.write('ip%s %s:%s -> %s:%s\n' %
                      (pkt.ip.version(),
                       pkt.ip.s_addr(), pkt.tcp.s_port(),
                       pkt.ip.d_addr(), pkt.tcp.d_port()))
