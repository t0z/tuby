try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

import sys
import time
import random
import select
import socket


def chk(data):
    x = sum(
        a + b * 256 for a, b
            in zip(data[::2], data[1::2] + b'\x00')) & 0xFFFFFFFF
    x = (x >> 16) + (x & 0xFFFF)
    x = (x >> 16) + (x & 0xFFFF)
    return (~x & 0xFFFF).to_bytes(2, 'little')


def ping(addr, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)\
            as conn:
        payload = random.randrange(0, 65536).to_bytes(2, 'big') + b'\x01\x00'
        packet = b'\x08\x00' + b'\x00\x00' + payload
        packet = b'\x08\x00' + chk(packet) + payload
        conn.connect((addr, 80))
        conn.sendall(packet)

        start = time.time()
        print "Start: %s" % start
        while select.select([conn], [], [],
                            max(0, start + timeout - time.time()))[0]:
            packet = conn.recv(1024)[20:]
            unchecked = packet[:2] + b'\0\0' + packet[4:]

            if packet == b'\0\0' + chk(unchecked) + payload:
                return time.time() - start
    return None


def helper(addr):
    addr = addr.encode('utf8').strip()
    elapsed = None
    try:
        elapsed = ping(addr)
    except Exception as e:
        TUBY.stderr.write("Error: %s\n" % e)
    TUBY.stdout.write('+ [ping] icmp://%s %s\n' %
                      (addr, elapsed if elapsed is not None else 'timeout'))

if len(sys.argv) > 3:
    helper(sys.argv[3].encode('utf8').strip())
else:
    for addr in TUBY.stdin:
        helper(addr)
