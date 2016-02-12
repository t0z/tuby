try:
    TUBY = TUBY  # @UndefinedVariable
except Exception:
    from tuby.core import TubyStream
    TUBY = TubyStream()

import json
packet = None
allip = {}
for data in TUBY.stdin:
    try:
        packet = json.loads(data)
    except Exception as e:
        TUBY.stderr('Exception: %s\n' % e)
        continue
    ip = None
    port = None
    for addr in ['s_addr', 'd_addr']:
        ip = packet[addr]
        port = packet['%s_port' % addr[0]]
        if ip in allip:
            allip[ip] = allip[ip] + 1
        else:
            allip[ip] = 1
            TUBY.stdout.write('[found.ip/%s] %s:%s\n' % (addr,
                                                        packet[addr], port))

#     TUBY.stdout.write('%s:%s %s:%s %s\n' % (packet['s_addr'],
#                                             packet['s_port'],
#                                             packet['d_addr'],
#                                             packet['d_port'],
#                                             packet['version']))
